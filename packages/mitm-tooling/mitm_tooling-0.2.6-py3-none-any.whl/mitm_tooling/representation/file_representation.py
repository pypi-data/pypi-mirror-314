import itertools
import os
from collections.abc import Iterable
from typing import BinaryIO, TextIO

import pandas as pd


from mitm_tooling.data_types import MITMDataType
from mitm_tooling.data_types.convert import convert_df
from mitm_tooling.definition import get_mitm_def, MITM, ConceptName
from mitm_tooling.definition.definition_tools import map_col_groups
from mitm_tooling.representation.common import guess_k
from mitm_tooling.utilities.io_utils import DataSink, DataSource, use_for_pandas_io, FilePath, ensure_directory_exists, ensure_ext
from mitm_tooling.utilities.python_utils import i_th


def mk_header_file_columns(k: int) -> list[str]:
    return ['kind', 'type'] + list(
        itertools.chain(*((f'a_{i}', f'a_dt_{i}') for i in range(1, k + 1))))


def mk_concept_file_header(mitm: MITM, concept: ConceptName, k: int) -> tuple[list[str], dict[str, MITMDataType]]:
    mitm_def = get_mitm_def(mitm)
    _, dts = map_col_groups(mitm_def, concept, {
        'kind': lambda: ('kind', MITMDataType.Text),
        'type': lambda: (mitm_def.get_properties(concept).typing_concept, MITMDataType.Text),
        'identity': lambda: mitm_def.resolve_identity_type(concept).items(),
        'inline': lambda: mitm_def.resolve_inlined_types(concept).items(),
        'foreign': lambda: [
            (name, dt) for fk_types in mitm_def.resolve_foreign_types(concept).values() for name, dt in
            fk_types.items()],
        'attributes': lambda: [(f'a_{i}', MITMDataType.Unknown) for i in range(1, k + 1)],
    })

    return list(dts.keys()), dict(dts)


def write_header_file(df: pd.DataFrame, sink: DataSink) -> None:
    if isinstance(sink, FilePath):
        ensure_directory_exists(sink)
    df.to_csv(sink, header=True, index=False, sep=';')


def write_data_file(df: pd.DataFrame, sink: DataSink, append: bool = False) -> None:
    if isinstance(sink, FilePath):
        ensure_directory_exists(sink)
    df.to_csv(sink, header=not append, index=False, sep=';', date_format='%Y-%m-%dT%H:%M:%S.%f%z')


def read_header_file(source: DataSource, normalize: bool = False) -> pd.DataFrame:
    with use_for_pandas_io(source) as f:
        df = pd.read_csv(f, sep=';')
        if normalize:
            k = guess_k(df)
            df = df.astype(pd.StringDtype()).reindex(columns=mk_header_file_columns(k))
        return df


def read_data_file(source: DataSource, target_mitm: MITM | None = None, target_concept: ConceptName | None = None,
                   normalize: bool = False) -> pd.DataFrame:
    with use_for_pandas_io(source) as f:
        df = pd.read_csv(f, sep=';', date_format='%Y-%m-%dT%H:%M:%S.%f%z', low_memory=False)
        if normalize and target_mitm and target_concept:
            k = guess_k(df)
            cols, column_dts = mk_concept_file_header(target_mitm, target_concept, k)
            df = df.reindex(columns=cols)
            convert_df(df, column_dts, inplace=True)
        return df
