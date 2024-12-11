import sqlalchemy as sa
from pydantic import AnyUrl
from sqlalchemy import Engine


def qualify(*, table: str, schema: str | None = None, column: str | None = None):
    res = table
    if schema is not None:
        res = schema + '.' + res
    if column is not None:
        res += '.' + column
    return res


def unqualify(n: str) -> list[str]:
    return n.split('.')


def create_sa_engine(db_url: AnyUrl, sqlite_extensions: list[str] | None = None, test_engine: bool = False,
                     **engine_kwargs) -> Engine:
    engine = sa.create_engine(str(db_url), **engine_kwargs)

    return engine
