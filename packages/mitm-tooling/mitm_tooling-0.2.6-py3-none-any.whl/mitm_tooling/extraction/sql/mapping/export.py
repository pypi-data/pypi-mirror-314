import dataclasses
import itertools
from collections.abc import Iterator
from typing import TYPE_CHECKING

import pandas as pd
import pydantic
import sqlalchemy as sa
from sqlalchemy.orm import Session

from mitm_tooling.definition import get_mitm_def, MITM, ConceptName
from ..data_models import DBMetaInfo, VirtualView
from ..data_models import SourceDBType, TableIdentifier
from ..transformation.db_transformation import TableNotFoundException
from ..transformation import PostProcessing
from .mapping import ConceptMapping, DataProvider, ConceptMappingException, InstancesProvider, \
    InstancesPostProcessor
from mitm_tooling.io import ZippedExport, StreamingZippedExport
from mitm_tooling.representation import HeaderEntry, Header, StreamingConceptData, StreamingMITMData, MITMData, mk_concept_file_header

STREAMING_CHUNK_SIZE = 100_000


class Exportable(pydantic.BaseModel):
    mitm: MITM
    data_providers: dict[ConceptName, list[DataProvider]]
    filename: str | None = None

    def execute_to_memory(self, db_session: Session, validate: bool = False) -> ZippedExport:
        header_entries = []

        tables = {}
        for c, dps in self.data_providers.items():

            dfs = []
            for dp in dps:
                df = dp.instance_provider.from_session(db_session)
                if validate:
                    raise NotImplementedError
                df = dp.instance_postprocessor.apply(df)
                dfs.append(df)
                header_entries += dp.header_entry_provider.from_df(df)

            tables[c] = pd.concat(dfs, axis='index', ignore_index=True)

        header = Header(mitm=self.mitm, header_entries=header_entries)

        filename = self.filename if self.filename else f'{self.mitm}.zip'

        return ZippedExport(mitm=self.mitm, filename=filename, mitm_data=MITMData(header=header, concept_dfs=tables))


    def stream_to_file(self, db_session: Session, validate: bool = False) -> StreamingZippedExport:

        data_sources = {}
        for c, dps in self.data_providers.items():
            k = max((dp.header_entry_provider.type_arity for dp in dps))
            concept_file_columns = mk_concept_file_header(self.mitm, c, k)[0]
            structure_df = pd.DataFrame(columns=concept_file_columns)

            chunk_iterators = []
            for dp in dps:
                def local_iter(dp: DataProvider, columns=concept_file_columns) -> Iterator[
                    tuple[pd.DataFrame, list[HeaderEntry]]]:
                    for df_chunk in dp.instance_provider.from_session_chunked(db_session, STREAMING_CHUNK_SIZE):
                        if validate:
                            raise NotImplementedError
                        df_chunk = df_chunk.reindex(columns=columns, copy=False)
                        yield dp.instance_postprocessor.apply(df_chunk), dp.header_entry_provider.from_df(df_chunk)

                chunk_iterators.append(local_iter(dp))

            data_sources[c] = StreamingConceptData(structure_df=structure_df, chunk_iterators=chunk_iterators)

        filename = self.filename if self.filename else f'{self.mitm}.zip'
        return StreamingZippedExport(mitm=self.mitm, filename=filename,
                                     streaming_mitm_data=StreamingMITMData(data_sources=data_sources))


class MappingExport(pydantic.BaseModel):
    mitm: MITM
    mapped_concepts: list[ConceptMapping]
    post_processing: PostProcessing | None = None
    filename: str | None = None

    def apply(self, db_metas: dict[SourceDBType, DBMetaInfo]) -> Exportable:
        data_providers: dict[ConceptName, list[DataProvider]] = {}

        meta = sa.MetaData(schema='export')
        for i, concept_mapping in enumerate(self.mapped_concepts):
            if concept_mapping.mitm != self.mitm:
                continue

            try:
                header_entry_provider, q = concept_mapping.apply(db_metas)
            except TableNotFoundException as e:
                raise ConceptMappingException(f'Concept Mapping failed due to: {repr(e)}')

            mitm_def = get_mitm_def(self.mitm)
            main_concept = mitm_def.get_parent(concept_mapping.concept)
            vv = VirtualView.from_from_clause(f'{main_concept}_{i}', q, meta, schema='export')
            instances_provider = InstancesProvider(virtual_view=vv)

            pp_transforms = []
            if self.post_processing is not None:
                pp_transforms = list(itertools.chain(
                    (tpp.transforms for tpp in self.post_processing.table_postprocessing if
                     TableIdentifier.check_equal(tpp.target_table, concept_mapping.base_table))))
            post_processor = InstancesPostProcessor(transforms=pp_transforms)

            if main_concept not in data_providers:
                data_providers[main_concept] = []
            data_providers[main_concept].append(
                DataProvider(instance_provider=instances_provider, instance_postprocessor=post_processor,
                             header_entry_provider=header_entry_provider))

        return Exportable(mitm=self.mitm, data_providers=data_providers, filename=self.filename)
