import logging
from functools import cached_property
from typing import Callable

import pydantic
from pydantic import Field

from ..data_models import DBMetaInfo, Queryable, TableIdentifier, SourceDBType, SchemaName, TableName
from ..data_models import VirtualView
from mitm_tooling.extraction.sql.transformation.db_transformation import TableTransforms, TableCreations, InvalidQueryException, \
    TransformationError, TableNotFoundException, ColumnNotFoundException

logger = logging.getLogger('api')


class VirtualViewCreation(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    name: TableName
    table_creation: TableCreations
    transforms: list[TableTransforms] | None = None
    schema_name: SchemaName = Field(alias='schema', default='virtual')

    @cached_property
    def table_identifier(self) -> TableIdentifier:
        return TableIdentifier(source=SourceDBType.VirtualDB, schema=self.schema_name, name=self.name)

    def create_queryable(self, db_metas: dict[SourceDBType, DBMetaInfo]) -> Queryable:
        from_clause = self.table_creation.make_from_clause(db_metas)

        if transforms := self.transforms:
            for t in transforms:
                from_clause = t.transform_from_clause(from_clause)
        return from_clause


def make_virtual_view(db_metas: dict[SourceDBType, DBMetaInfo],
                      vv_creation_request: VirtualViewCreation,
                      override_if_exists: bool = False,
                      queryable_verifier: Callable[[Queryable], bool] | None = None) -> VirtualView | None:
    try:
        from_clause = vv_creation_request.create_queryable(db_metas)

        if queryable_verifier is not None:
            try:
                if not queryable_verifier(from_clause):
                    raise InvalidQueryException
            except Exception as e:
                raise InvalidQueryException(
                    f'Virtual view query: {from_clause} was not executable on the connected DB.').with_traceback(
                    e.__traceback__)

        vv = VirtualView.from_from_clause(vv_creation_request.name, from_clause,
                                          db_metas[SourceDBType.VirtualDB].sa_meta,
                                          schema=vv_creation_request.schema_name,
                                          delete_if_exists=override_if_exists)

        return vv
    except (TransformationError, TableNotFoundException, ColumnNotFoundException, InvalidQueryException) as e:
        logger.error(f'Error during virtual view creation: {e:r}')
        raise e
