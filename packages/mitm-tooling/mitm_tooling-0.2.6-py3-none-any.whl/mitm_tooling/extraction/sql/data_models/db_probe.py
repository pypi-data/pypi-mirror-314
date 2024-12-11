import logging
from typing import Any

import pydantic
from pydantic import NonNegativeInt, Field

from mitm_tooling.data_types.data_types import MITMDataType
from .db_meta import TableMetaInfoBase, DBMetaInfoBase, DBMetaInfo, ColumnName
from .probe_models import SampleSummary
from .table_identifiers import ShortTableIdentifier

logger = logging.getLogger('api')


class TableProbeMinimal(pydantic.BaseModel):
    row_count: NonNegativeInt
    inferred_types: dict[ColumnName, MITMDataType]
    sample_summaries: dict[ColumnName, SampleSummary]


class TableProbeBase(TableProbeMinimal):
    model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)

    table_meta: TableMetaInfoBase
    sampled_values: dict[ColumnName, list[Any]]


class TableProbe(TableProbeBase):
    ...


class DBProbeMinimal(pydantic.BaseModel):
    table_probes: dict[ShortTableIdentifier, TableProbeMinimal] = Field(default_factory=dict)


class DBProbeBase(DBProbeMinimal):
    db_meta: DBMetaInfoBase
    table_probes: dict[ShortTableIdentifier, TableProbeBase] = Field(default_factory=dict)


class DBProbe(DBProbeBase):
    db_meta: DBMetaInfo
    table_probes: dict[ShortTableIdentifier, TableProbe] = Field(default_factory=dict)

    def update_meta(self, db_meta: DBMetaInfo):
        if self.db_meta:
            for new_ti, new_table in db_meta.tables.items():
                if (table := self.db_meta.tables.get(new_ti, None)) is not None:
                    if table != new_table:
                        # remove associated probe
                        logger.info(f'Removed table probe of {new_ti} due to metadata refresh.')
                        self.table_probes.pop(new_ti, None)
                    # self.table_probes.get(new_ti).table_info = new_table
        self.db_meta = db_meta

    def update_probes(self, *probes: tuple[ShortTableIdentifier, TableProbe]):
        for ti, tp in probes:
            self.table_probes[ti] = tp

    def drop_probes(self, *to_drop: ShortTableIdentifier):
        for ti in to_drop:
            if ti in self.table_probes:
                del self.table_probes[ti]
