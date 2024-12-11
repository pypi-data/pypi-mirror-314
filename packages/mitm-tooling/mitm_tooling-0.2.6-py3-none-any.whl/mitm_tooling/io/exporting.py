import dataclasses

import pydantic

import io
import logging
import os
import zipfile
from abc import ABC, abstractmethod
from typing import BinaryIO, Iterator

import pandas as pd

from mitm_tooling.definition import MITM, ConceptName, get_mitm_def
from mitm_tooling.representation.intermediate_representation import HeaderEntry, Header, StreamingConceptData, MITMData, \
    StreamingMITMData
from mitm_tooling.representation.file_representation import write_header_file, write_data_file
from mitm_tooling.utilities.io_utils import DataSink, ByteSink, use_bytes_io, ensure_ext

logger = logging.getLogger('api')


class FileExport(pydantic.BaseModel, ABC):
    mitm: MITM
    filename: str

    @abstractmethod
    def write(self, sink: DataSink, **kwargs):
        pass

    def to_buffer(self) -> io.BytesIO:
        buffer = io.BytesIO()
        self.write(buffer)
        buffer.seek(0)
        return buffer

    def into_file(self, path: os.PathLike):
        self.write(path)


class ZippedExport(FileExport):
    mitm_data: MITMData

    def write(self, sink: DataSink, **kwargs):
        if not isinstance(sink, ByteSink):
            logger.error(f'Attempted to write to unsupported data sink: {sink}.')
            return

        mitm_def = get_mitm_def(self.mitm)
        with use_bytes_io(sink, expected_file_ext='.zip', mode='wb', create_file_if_necessary=True) as f:
            with zipfile.ZipFile(f, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                with zf.open('header.csv', 'w') as hf:
                    write_header_file(self.mitm_data.header.generate_header_df(), hf)
                for c, df in self.mitm_data:
                    fn = ensure_ext(mitm_def.get_properties(c).plural, '.csv')
                    with zf.open(fn, 'w') as cf:
                        write_data_file(df, cf)
                        logger.debug(f'Wrote {len(df)} rows to {fn} (in-memory export).')


class StreamingZippedExport(FileExport):
    streaming_mitm_data: StreamingMITMData

    def write(self, sink: ByteSink, **kwargs):
        if not isinstance(sink, ByteSink):
            logger.error(f'Attempted to write to unsupported data sink: {sink}.')
            return

        mitm_def = get_mitm_def(self.mitm)
        collected_header_entries = []
        with use_bytes_io(sink, expected_file_ext='.zip', mode='wb', create_file_if_necessary=True) as f:
            with zipfile.ZipFile(f, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
                for c, concept_data in self.streaming_mitm_data:
                    fn = ensure_ext(mitm_def.get_properties(c).plural, '.csv')
                    with zf.open(fn, 'w') as cf:
                        write_data_file(concept_data.structure_df, cf, append=False)
                        for df_chunks in concept_data.chunk_iterators:
                            for df_chunk, header_entries in df_chunks:
                                collected_header_entries.extend(header_entries)
                                write_data_file(df_chunk, cf, append=True)
                                logger.debug(f'Wrote {len(df_chunk)} rows to {fn} (streaming export).')

                with zf.open('header.csv', 'w') as hf:
                    header_df = Header(mitm=self.mitm, header_entries=collected_header_entries).generate_header_df()
                    write_header_file(header_df, hf)
