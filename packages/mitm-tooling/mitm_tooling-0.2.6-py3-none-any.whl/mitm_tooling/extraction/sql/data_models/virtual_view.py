import logging
from typing import Self

import pydantic
import sqlalchemy as sa
from pydantic import Field

from mitm_tooling.data_types import get_sa_sql_type, SQL_DataType
from mitm_tooling.utilities.sql_utils import qualify
from .db_meta import TableMetaInfoBase, TableMetaInfo, DBMetaInfo
from .table_identifiers import SchemaName, TableName, ShortTableIdentifier

logger = logging.getLogger('api')

VIRTUAL_DB_DEFAULT_SCHEMA = 'virtual'


class VirtualViewBase(pydantic.BaseModel):
    table_meta: TableMetaInfoBase


class VirtualView(VirtualViewBase):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    table_meta: TableMetaInfo
    from_clause: sa.FromClause
    sa_table: sa.Table

    @classmethod
    def from_from_clause(cls, name: str, from_clause: sa.FromClause, meta: sa.MetaData,
                         schema: SchemaName = 'virtual', delete_if_exists: bool = True) -> Self | None:
        cols = [sa.Column(n, c.type, primary_key=c.primary_key) for n, c in from_clause.columns.items()]

        if (t := meta.tables.get(qualify(schema=schema, table=name), None)) is not None:
            if delete_if_exists:
                meta.remove(t)
            else:
                return

        virtual_table = sa.Table(name, meta, *cols, schema=schema)
        tm = TableMetaInfo.from_sa_table(virtual_table, queryable_source=from_clause, default_schema=schema)
        return cls(table_meta=tm, from_clause=from_clause, sa_table=virtual_table)

    def as_compiled(self, dialect: sa.Dialect) -> 'CompiledVirtualView':
        compiled = self.from_clause.select().compile(dialect=dialect, compile_kwargs={"literal_binds": True})
        contains_binds = len(compiled.binds) > 0
        tm = self.table_meta
        if contains_binds:
            logger.warning(f'Compiled virtual view {tm.name} contains binds:\n{compiled}')
        # col_dtypes = [dt for dt in tm.sql_column_types]
        return CompiledVirtualView(name=tm.name, schema_name=tm.schema_name, dialect=dialect.name,
                                   compiled_sql=str(compiled.statement), columns=tm.columns,
                                   column_dtypes=tm.sql_column_types)


class TypedRawQuery(pydantic.BaseModel):
    dialect: str
    compiled_sql: str
    columns: list[str]
    column_dtypes: list[SQL_DataType]

    def to_from_clause(self) -> sa.FromClause:
        cols = [sa.Column(c, get_sa_sql_type(dt)) for c, dt in zip(self.columns, self.column_dtypes)]
        return sa.text(self.compiled_sql).columns(*cols).subquery()


class CompiledVirtualView(TypedRawQuery):
    name: TableName
    schema_name: SchemaName

    def to_virtual_view(self, meta: sa.MetaData, delete_if_exists: bool = True) -> VirtualView:
        return VirtualView.from_from_clause(self.name, self.to_from_clause(), meta,
                                            schema=self.schema_name, delete_if_exists=delete_if_exists)


class VirtualDBBase(pydantic.BaseModel):
    virtual_views: dict[SchemaName, dict[TableName, VirtualViewBase]] = Field(default_factory=dict)


class VirtualDB(VirtualDBBase):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    virtual_views: dict[SchemaName, dict[TableName, VirtualView]] = Field(default_factory=dict)
    sa_meta: sa.MetaData = sa.MetaData(schema='virtual')

    @pydantic.computed_field(repr=False)
    @property
    def views(self) -> dict[ShortTableIdentifier, VirtualView]:
        return {vv.table_meta.short_table_identifier: vv for schema, views in self.virtual_views.items() for view, vv in
                views.items()}

    def put_view(self, vv: VirtualView):
        schema = vv.table_meta.schema_name
        if schema not in self.virtual_views:
            self.virtual_views[schema] = {}
        self.virtual_views[schema][vv.table_meta.name] = vv

    def get_view(self, schema: SchemaName, view: TableName) -> VirtualView | None:
        return self.virtual_views.get(schema, {}).get(view, None)

    def drop_view(self, schema: SchemaName, view: TableName):
        tm = self.get_view(schema, view)
        if tm is not None:
            self.sa_meta.remove(tm.sa_table)
            del self.virtual_views[schema][view]
            if len(self.virtual_views[schema]) == 0:
                del self.virtual_views[schema]

    def to_db_meta_info(self) -> DBMetaInfo:
        return DBMetaInfo(db_structure={schema: {view: vv.table_meta for view, vv in views.items()} for schema, views in
                                        self.virtual_views.items()}, sa_meta=self.sa_meta,
                          default_schema=VIRTUAL_DB_DEFAULT_SCHEMA)
