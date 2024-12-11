import enum
import json
from typing import Callable

import pandas as pd
import pydantic
import sqlalchemy as sa
from sqlalchemy.sql import sqltypes

SA_SQLTypeClass = type[sa.types.TypeEngine]

SA_SQLTypeName = str
PandasCast = Callable[[pd.Series], pd.Series]


class MITMDataType(enum.StrEnum):
    Text = 'text'
    Json = 'json'
    Integer = 'integer'
    Numeric = 'numeric'
    Boolean = 'boolean'
    Datetime = 'datetime'
    # Binary = 'binary'
    # Categorical = 'categorical'
    Unknown = 'unknown'
    Infer = 'infer'

    @property
    def sa_sql_type(self) -> SA_SQLTypeClass | None:
        return mitm_sql_type_map.get(self)

    @property
    def pandas_cast(self) -> PandasCast | None:
        return mitm_pandas_type_mappers.get(self)

    @property
    def sql_type_str(self) -> str:
        return self.sa_sql_type.__name__

    def wrap(self) -> 'WrappedMITMDataType':
        return WrappedMITMDataType(mitm=self)


EitherDataType = MITMDataType | SA_SQLTypeName


class WrappedMITMDataType(pydantic.BaseModel):
    mitm: MITMDataType


SQL_DataType = WrappedMITMDataType | SA_SQLTypeName


def sa_sql_to_mitm_type(sa_type: SA_SQLTypeClass) -> MITMDataType:
    matches = [dt for c, dt in sql_mitm_type_map.items() if isinstance(sa_type, c)]
    return matches[-1] if len(matches) > 0 else MITMDataType.Unknown


def mitm_to_sql_type(mitm_type: MITMDataType) -> SA_SQLTypeClass | None:
    return mitm_type.sa_sql_type


def mitm_to_pandas(mitm_type: MITMDataType) -> PandasCast | None:
    return mitm_type.pandas_cast


def get_sa_sql_type(type_name: EitherDataType | WrappedMITMDataType) -> SA_SQLTypeClass | None:
    if isinstance(type_name, MITMDataType):
        return type_name.sa_sql_type
    elif isinstance(type_name, WrappedMITMDataType):
        return type_name.mitm.sa_sql_type
    else:
        if type_name and (t := getattr(sqltypes, type_name, None)):
            if isinstance(t, type):
                return t


def get_pandas_cast(type_name: EitherDataType | WrappedMITMDataType) -> PandasCast | None:
    if isinstance(type_name, MITMDataType):
        return type_name.pandas_cast
    elif isinstance(type_name, WrappedMITMDataType):
        return type_name.mitm.pandas_cast
    else:
        from sqlalchemy.sql import sqltypes
        if type_name and (t := getattr(sqltypes, type_name, None)):
            if isinstance(t, type):
                return sa_sql_to_mitm_type(t).pandas_cast


def get_sa_sql_classes():
    import sys, inspect
    names, clss = zip(*inspect.getmembers(sys.modules[__name__],
                                          lambda member: inspect.isclass(member) and member.__module__ == __name__))
    return names


sql_mitm_type_map: dict[SA_SQLTypeClass, MITMDataType] = {
    sqltypes.String: MITMDataType.Text,
    sqltypes.Text: MITMDataType.Text,
    sqltypes.DateTime: MITMDataType.Datetime,
    sqltypes.JSON: MITMDataType.Json,
    sqltypes.Boolean: MITMDataType.Boolean,
    sqltypes.Integer: MITMDataType.Integer,
    sqltypes.Numeric: MITMDataType.Numeric,
    sqltypes.Float: MITMDataType.Numeric,
    # sqltypes.Enum: MITMDataType.Categorical,
    # sqltypes.LargeBinary: MITMDataType.Binary,
    # sqltypes.BINARY: MITMDataType.Binary,
}

mitm_sql_type_map: dict[MITMDataType, SA_SQLTypeClass] = {
    MITMDataType.Text: sqltypes.String,
    MITMDataType.Datetime: sqltypes.DATETIME_TIMEZONE,
    MITMDataType.Json: sqltypes.JSON,
    MITMDataType.Boolean: sqltypes.Boolean,
    MITMDataType.Integer: sqltypes.Integer,
    MITMDataType.Numeric: sqltypes.Float,
    MITMDataType.Unknown: None,
    MITMDataType.Infer: None,
    # MITMDataType.Binary: sqltypes.LargeBinary,
    # MITMDataType.Categorical: sqltypes.Enum
}

mitm_pandas_type_mappers: dict[MITMDataType, PandasCast] = {
    MITMDataType.Text: lambda s: s.astype(pd.StringDtype()),
    MITMDataType.Datetime: lambda s: pd.to_datetime(s, utc=True, errors='coerce', format='mixed'),
    MITMDataType.Json: lambda s: s.astype(pd.StringDtype()).apply(json.loads),
    MITMDataType.Boolean: lambda s: s.astype('Boolean'),
    MITMDataType.Integer: lambda s: s.astype('Int64'),
    MITMDataType.Numeric: lambda s: s.astype('Float64'),
    MITMDataType.Unknown: lambda s: s,
    MITMDataType.Infer: lambda s: pd.Series.convert_dtypes(s),
}
