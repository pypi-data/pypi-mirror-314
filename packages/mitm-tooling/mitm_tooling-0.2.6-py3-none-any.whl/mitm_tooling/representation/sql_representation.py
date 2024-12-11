from collections import defaultdict
from collections.abc import Callable, Iterator, Generator, Mapping

import sqlalchemy as sa
import sqlalchemy.sql.schema
from pydantic_core import Url

from mitm_tooling.definition import MITMDefinition, ConceptProperties, OwnedRelations
from mitm_tooling.data_types import MITMDataType
from mitm_tooling.definition import ConceptName, MITM, get_mitm_def, ConceptKind, ConceptLevel, RelationName
from mitm_tooling.definition.definition_tools import map_col_groups, ColGroupMaps
from .intermediate_representation import Header, MITMData, ColumnName
from mitm_tooling.utilities.sql_utils import create_sa_engine
from mitm_tooling.utilities import python_utils
from mitm_tooling.utilities.sql_utils import qualify


def mk_concept_table_name(mitm: MITM, concept: ConceptName) -> str:
    return get_mitm_def(mitm).get_properties(concept).plural


def mk_type_table_name(mitm: MITM, concept: ConceptName, type_name: RelationName) -> str:
    return get_mitm_def(mitm).get_properties(concept).key + '_' + type_name.lower()


def mk_link_table_name(mitm: MITM, concept: ConceptName, type_name: RelationName, fk_name: RelationName) -> str:
    return mk_type_table_name(mitm, concept, type_name) + '_' + fk_name.lower()


def has_type_tables(mitm: MITM, concept: ConceptName) -> bool:
    return get_mitm_def(mitm).get_properties(concept).permit_attributes


def pick_table_pk(mitm: MITM, concept: ConceptName, created_columns: Mapping[RelationName, sa.Column]) -> list[
    tuple[RelationName, sa.Column]]:
    mitm_def = get_mitm_def(mitm)
    concept_properties, concept_relations = mitm_def.get(concept)

    names, mapped_names = map_col_groups(mitm_def, concept, {
        'kind': lambda: 'kind',
        'type': lambda: concept_properties.typing_concept,
        'identity': lambda: list(concept_relations.identity)
    })

    return python_utils.pick_from_mapping(created_columns, names)


def mk_table(meta: sa.MetaData, mitm: MITM, concept: ConceptName, table_name: str, col_group_maps: ColGroupMaps,
             additional_schema_item_maker: Callable[
                                               [MITM, ConceptName, ConceptProperties, OwnedRelations,
                                                dict[RelationName, sa.Column], list[tuple[RelationName, sa.Column]]],
                                               Generator[
                                                   sqlalchemy.sql.schema.SchemaItem, None, None]] | None = None) -> \
        tuple[
            sa.Table, dict[RelationName, sa.Column], list[tuple[RelationName, sa.Column]]]:
    mitm_def = get_mitm_def(mitm)
    concept_properties, concept_relations = mitm_def.get(concept)

    columns, created_columns = map_col_groups(mitm_def, concept, col_group_maps, ensure_unique=True)

    ref_columns = pick_table_pk(mitm, concept, created_columns)

    constraints: list[sa.sql.schema.SchemaItem] = []
    if concept_relations.identity:
        constraints.append(sa.PrimaryKeyConstraint(*python_utils.i_th(1)(ref_columns)))

    if additional_schema_item_maker:
        constraints.extend(iter(
            additional_schema_item_maker(mitm, concept, concept_properties, concept_relations, created_columns,
                                         ref_columns)))
        print(constraints)

    return sa.Table(table_name, meta, *columns, *constraints), created_columns, ref_columns


def mk_db_schema(header: Header) -> tuple[sa.MetaData, dict[ConceptName, dict[str, sa.Table]]]:
    mitm_def = get_mitm_def(header.mitm)
    meta = sa.MetaData()

    tables: dict[ConceptName, dict[str, sa.Table]] = {}
    views: dict[ConceptName, sa.Table] = {}

    for concept in mitm_def.main_concepts:
        concept_properties, concept_relations = mitm_def.get(concept)

        table_name = mk_concept_table_name(header.mitm, concept)

        t, t_columns, t_ref_columns = mk_table(meta, header.mitm, concept, table_name, {
            'kind': lambda: ('kind', sa.Column('kind', MITMDataType.Text.sa_sql_type, nullable=False)),
            'type': lambda: (concept_properties.typing_concept, sa.Column(concept_properties.typing_concept,
                                                                          MITMDataType.Text.sa_sql_type,
                                                                          nullable=False)),
            'identity': lambda: [(name, sa.Column(name, dt.sa_sql_type, nullable=False)) for
                                 name, dt in
                                 mitm_def.resolve_identity_type(concept).items()],
            'inline': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                               mitm_def.resolve_inlined_types(concept).items()],
            'foreign': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for _, resolved_fk in
                                mitm_def.resolve_foreign_types(concept).items() for name, dt in
                                resolved_fk.items()]
        })

    for he in header.header_entries:
        he_concept = he.concept
        if has_type_tables(header.mitm, he_concept):
            concept_properties, concept_relations = mitm_def.get(he_concept)

            def foreign_key_constraints(mitm, concept, concept_properties, concept_relations, created_columns,
                                        ref_columns):
                # self_fk
                parent_table = mk_concept_table_name(mitm, concept)
                cols, refcols = zip(
                    *((c, qualify(table=parent_table, column=s)) for s, c in ref_columns))
                yield sa.ForeignKeyConstraint(name='parent', columns=cols, refcolumns=refcols)
                for fk_name, fk_info in concept_relations.foreign.items():
                    cols, refcols = zip(*fk_info.fk_relations.items())
                    fkc = sa.ForeignKeyConstraint(name=fk_name, columns=[created_columns[c] for c in cols], refcolumns=[
                        # sa.literal_column(qualify(table=mk_concept_table_name(mitm, fk_info.target_concept), column=c))
                        qualify(table=mk_concept_table_name(mitm, fk_info.target_concept), column=c)
                        for c in refcols])
                    yield fkc

            table_name = mk_type_table_name(header.mitm, he_concept, he.type_name)

            t, t_columns, t_ref_columns = mk_table(meta, header.mitm, he_concept, table_name, {
                'kind': lambda: ('kind', sa.Column('kind', MITMDataType.Text.sa_sql_type, nullable=False)),
                'type': lambda: (concept_properties.typing_concept, sa.Column(concept_properties.typing_concept,
                                                                              MITMDataType.Text.sa_sql_type,
                                                                              nullable=False)),
                'identity': lambda: [(name, sa.Column(name, dt.sa_sql_type, nullable=False)) for
                                     name, dt in
                                     mitm_def.resolve_identity_type(he_concept).items()],
                'inline': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                                   mitm_def.resolve_inlined_types(he_concept).items()],
                'foreign': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for _, resolved_fk in
                                    mitm_def.resolve_foreign_types(he_concept).items() for name, dt in
                                    resolved_fk.items()],
                'attributes': lambda: [(name, sa.Column(name, dt.sa_sql_type)) for name, dt in
                                       zip(he.attributes, he.attribute_dtypes)],
            }, additional_schema_item_maker=foreign_key_constraints)

            if he_concept not in tables:
                tables[he_concept] = {}
            tables[he_concept][he.type_name] = t

    # for concept, members in concept_level_view_members.items():

    #    view_selection = sa.union_all(*(sa.select(*pk_cols) for pk_cols in members))

    #    views[concept] = view.create_materialized_view(mk_concept_table_name(header.mitm, concept), view_selection,

    #                                                   meta)

    return meta, tables  # , views


def insert_db_instances(engine: sa.Engine, meta: sa.MetaData, mitm_data: MITMData):
    with engine.connect() as conn:
        mitm = mitm_data.header.mitm

        for concept, df in mitm_data:
            concept_table = mk_concept_table_name(mitm, concept)
            t_concept = meta.tables[concept_table]
            ref_cols = pick_table_pk(mitm, concept, t_concept.columns)
            parent_insert = t_concept.insert().values(df[[c.name for c in t_concept.columns]].to_dict('records'))
            conn.execute(parent_insert)

            if has_type_tables(mitm, concept):
                concept_properties, concept_relations = get_mitm_def(mitm).get(concept)
                for typ, idx in df.groupby(concept_properties.typing_concept).groups.items():
                    type_df = df.loc[idx]
                    t_type = meta.tables[mk_type_table_name(mitm, concept, str(typ))]
                    sub_insert = t_type.insert().values(type_df[[c.name for c in t_type.columns]].to_dict('records'))
                    conn.execute(sub_insert)
        conn.commit()


def insert_mitm_data(engine: sa.Engine, mitm_data: MITMData) -> tuple[
    sa.MetaData, dict[ConceptName, dict[str, sa.Table]]]:
    meta, tables = mk_db_schema(mitm_data.header)
    meta.create_all(engine)
    insert_db_instances(engine, meta, mitm_data)
    return meta, tables


def mk_sqlite(mitm_data: MITMData, file_path: str | None = ':memory:') -> tuple[
    sa.Engine, sa.MetaData, dict[ConceptName, dict[str, sa.Table]]]:
    engine = create_sa_engine(Url(f'sqlite:///{file_path}'))
    meta, tables = insert_mitm_data(engine, mitm_data)
    print(meta.tables)
    print([f'{t.name}: {t.columns} {t.constraints}' for ts in tables.values() for t in ts.values()])
    meta.create_all(engine)
    return engine, meta, tables
