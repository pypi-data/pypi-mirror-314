import pandas as pd

from .data_types import MITMDataType


class ColumnDataTypeConversionException(Exception):
    pass


def convert_df(df: pd.DataFrame, data_types: dict[str, MITMDataType], inplace=False):
    res = pd.DataFrame(index=df.index) if not inplace else df

    for col, dt in data_types.items():
        try:
            #if inplace:
            #    df[col] = convert_df_col(df, col, dt, inplace=False)
            #else:
            res[col] = convert_df_col(df, col, dt, inplace=False)
        except Exception as e:
            raise ColumnDataTypeConversionException(f'Conversion of feature \'{col}\' to {dt} failed:\n{e}')

    return res


def convert_df_col(df: pd.DataFrame, col: str, data_type: MITMDataType, inplace=False):
    cast = data_type.pandas_cast(df[col])
    if inplace:
        cast[col] = cast
    return cast


def convert_series(s: pd.Series, data_type: MITMDataType) -> pd.Series:
    return data_type.pandas_cast(s)
