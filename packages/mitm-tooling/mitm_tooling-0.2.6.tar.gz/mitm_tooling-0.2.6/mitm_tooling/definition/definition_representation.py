import dataclasses
import enum
import itertools
from functools import cached_property
from typing import Literal, Self

import pydantic
from pydantic import Field

from mitm_tooling.data_types.data_types import MITMDataType
from mitm_tooling.utilities.python_utils import unpack_singleton, map_vals, normalize_list_of_mixed, combine_dicts

COLUMN_GROUPS = Literal['kind', 'type', 'identity-relations', 'inline-relations', 'foreign-relations', 'attributes']
CANON_COLUMN_GROUP_ORDERING: tuple[COLUMN_GROUPS, ...] = (
    'kind', 'type', 'identity-relations', 'inline-relations', 'foreign-relations', 'attributes')
mitm_data_types = [v for v in MITMDataType]
ConceptName = str
RelationName = str


class ConceptLevel(enum.StrEnum):
    Main = 'main'
    Sub = 'sub'
    Weak = 'weak'


class ConceptKind(enum.StrEnum):
    Concrete = 'concrete'
    Abstract = 'abstract'


class MITM(enum.StrEnum):
    MAED = 'MAED'
    OCEL2 = 'OCEL2'
    # DPPD = 'DPPD'


class ForeignRelationInfo(pydantic.BaseModel):
    target_concept: ConceptName
    fk_relations: dict[RelationName, RelationName]
    # referred_column_concepts: dict[RelationName, ConceptName]


class OwnedRelations(pydantic.BaseModel):
    identity: dict[RelationName, ConceptName]
    inline: dict[RelationName, ConceptName]
    foreign: dict[RelationName, ForeignRelationInfo]

    def foreign_relations_to_concept(self, concept: ConceptName) -> dict[
        RelationName, dict[RelationName, RelationName]]:
        return {n: fk_rel_info.fk_relations for n, fk_rel_info in self.foreign.items() if
                fk_rel_info.target_concept == concept}


class ConceptProperties(pydantic.BaseModel):
    nature: tuple[ConceptLevel, ConceptKind]
    key: str
    plural: str
    typing_concept: ConceptName = 'type'
    column_group_ordering: tuple[COLUMN_GROUPS, ...] = CANON_COLUMN_GROUP_ORDERING
    permit_attributes: bool = True

    def inheritable_props(self):
        props = dict(self.__dict__)
        del props['nature']
        del props['key']
        return props


class MITMDefinition(pydantic.BaseModel):
    main_concepts: set[ConceptName]
    weak_concepts: dict[ConceptName, MITMDataType]
    sub_concepts: dict[ConceptName, set[ConceptName]]
    concept_relations: dict[ConceptName, OwnedRelations]
    concept_properties: dict[ConceptName, ConceptProperties]

    @pydantic.computed_field()
    @cached_property
    def leaf_concepts(self) -> set[ConceptName]:
        return {c for c in self.main_concepts if c not in self.sub_concepts} | {sc for c in self.main_concepts for sc in
                                                                                self.sub_concepts.get(c, [])}

    @pydantic.computed_field()
    @cached_property
    def abstract_concepts(self) -> set[ConceptName]:
        return {c for c in self.sub_concepts}

    @pydantic.computed_field()
    @cached_property
    def parent_concepts_map(self) -> dict[ConceptName, ConceptName]:
        return {sub: c for c, subs in self.sub_concepts.items() for sub in subs}

    @property
    def inverse_concept_key_map(self) -> dict[str, ConceptName]:
        return {cp.key: c for c, cp in self.concept_properties.items()}

    def get_parent(self, concept: ConceptName) -> ConceptName | None:
        if concept in self.main_concepts:
            return concept
        elif concept in (pm := self.parent_concepts_map):
            return pm[concept]

    def get(self, concept: ConceptName) -> tuple[ConceptProperties, OwnedRelations]:
        a, b = self.get_properties(concept), self.get_relations(concept)
        return a, b

    def get_properties(self, concept: ConceptName) -> ConceptProperties | None:
        return self.concept_properties.get(concept, None)

    def get_relations(self, concept: ConceptName) -> OwnedRelations | None:
        return self.concept_relations.get(self.get_parent(concept), None)

    def get_identity(self, concept: ConceptName) -> dict[RelationName, ConceptName]:
        return self.get_relations(concept).identity

    def resolve_types(self, arg: dict[RelationName, ConceptName]) -> dict[RelationName, MITMDataType]:
        return {relation_name: self.weak_concepts[target_concept] for relation_name, target_concept in arg.items()}

    def resolve_inlined_types(self, concept: ConceptName) -> dict[RelationName, MITMDataType]:
        return self.resolve_types(self.get_relations(concept).inline)

    def resolve_identity_type(self, concept: ConceptName) -> dict[RelationName, MITMDataType]:
        return self.resolve_types(self.get_relations(concept).identity)

    def resolve_foreign_types(self, concept: ConceptName) -> dict[
        RelationName, dict[RelationName, MITMDataType]]:
        return {fk_name: self.resolve_types(
            {name: self.get_relations(fk_info.target_concept).identity[target_name] for name, target_name in
             fk_info.fk_relations.items()}) for fk_name, fk_info in self.get_relations(concept).foreign.items()}


class OwnedRelationsFile(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True)

    identity: dict[RelationName, ConceptName] = Field(default_factory=dict)
    inline: dict[RelationName, ConceptName] = Field(default_factory=dict)
    foreign: dict[RelationName, dict[ConceptName, dict[RelationName, RelationName] | list[RelationName]]] = Field(
        default_factory=dict)

    def to_definition(self) -> OwnedRelations:
        def clean(d):
            k, v = unpack_singleton(d)
            return ForeignRelationInfo(target_concept=k, fk_relations=v)

        return OwnedRelations(identity=self.identity, inline=self.inline, foreign=map_vals(self.foreign, clean))


class Meta(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra='allow')

    keys: dict[str, ConceptName] | None = Field(default_factory=dict)
    plurals: dict[ConceptName, str] | None = Field(default_factory=dict)


class ConceptPropertiesFile(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True, extra='allow')

    typing_concept: ConceptName | None = Field(alias='typing-concept', default='type')
    permit_attributes: bool = Field(alias='permit-attributes', default=True)
    key: str | None = None
    plural: str | None = None
    override_column_group_ordering: list[COLUMN_GROUPS] | None = Field(alias='override-column-group-ordering',
                                                                       default=None)

    def to_definition(self, concept: ConceptName, whole_def: 'MITMDefinitionFile',
                      **inherited_kwargs) -> ConceptProperties:
        meta = whole_def.meta
        key = self.key
        if concept in meta.keys:
            key = meta.keys[concept]
        if concept in meta.plurals:
            key = meta.plurals[concept]
        if key is None:
            key = concept

        if concept in whole_def.weak_concepts:
            nature = ConceptLevel.Weak, ConceptKind.Concrete
        else:
            cs = normalize_list_of_mixed(whole_def.concepts)
            concept_level = ConceptLevel.Main if concept in cs else ConceptLevel.Sub
            concept_kind = ConceptKind.Concrete if cs.get(concept, None) is None else ConceptKind.Abstract
            nature = concept_level, concept_kind

        kwargs = combine_dicts(inherited_kwargs,
                               {'typing_concept': self.typing_concept, 'permit_attributes': self.permit_attributes,
                                'plural': self.plural}, {'plural': concept + 's'})

        opt_kwargs = {}
        if self.override_column_group_ordering is not None:
            opt_kwargs['column_group_ordering'] = tuple(
                list(self.override_column_group_ordering) + [g for g in CANON_COLUMN_GROUP_ORDERING if
                                                             g not in self.override_column_group_ordering])
        kwargs = combine_dicts(kwargs, opt_kwargs)
        return ConceptProperties(nature=nature, key=key, **kwargs)


class MITMDefinitionFile(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    mitm: MITM
    meta: Meta = Field(default_factory=Meta)
    concepts: list[ConceptName | dict[ConceptName, list[ConceptName]]] = Field(default_factory=list)
    weak_concepts: dict[ConceptName, MITMDataType] = Field(default_factory=dict, alias='weak-concepts')
    concept_properties: dict[ConceptName, ConceptPropertiesFile] = Field(default_factory=dict,
                                                                         alias='concept-properties')
    owned_relations: dict[ConceptName, OwnedRelationsFile] = Field(default_factory=dict, alias='owned-relations')
    # not implemented
    unowned_relations: dict[RelationName, OwnedRelationsFile] | None = Field(default=None,
                                                                             alias='unowned-relations')

    @pydantic.model_validator(mode='after')
    def check_fks(self) -> Self:
        for concept, owned_rels in self.owned_relations.items():
            for q, (target_concept, fk_rel) in map_vals(owned_rels.foreign, unpack_singleton).items():
                if set(fk_rel.values()) != set(self.owned_relations[target_concept].identity):
                    raise ValueError(
                        'foreign relation declaration does not map to identity relations of target concept')
        return self

    @pydantic.model_validator(mode='after')
    def check_target_concepts(self) -> Self:
        for concept, owned_rels in self.owned_relations.items():
            if not set(owned_rels.identity.values()) <= set(self.weak_concepts):
                raise ValueError('not all target concepts of the identity relations are weak concepts')
            if not set(owned_rels.inline.values()) <= set(self.weak_concepts):
                raise ValueError('not all target concepts of the inline relations are weak concepts')
        return self

    def to_definition(self) -> MITMDefinition:
        main_concepts = set()
        sub_concepts = {}
        for c in self.concepts:
            if isinstance(c, str):
                main_concepts.add(c)
            elif isinstance(c, dict):
                concept, sub = next(iter(c.items()))
                main_concepts.add(concept)
                sub_concepts[concept] = set(sub)
        concept_relations = {c: self.owned_relations[c].to_definition() for c in main_concepts if
                             c in self.owned_relations}
        del c

        def handle_properties(c, **kwargs) -> ConceptProperties:
            cp = self.concept_properties.get(c, ConceptPropertiesFile()).to_definition(c, self, **kwargs)
            concept_properties[c] = cp
            return cp

        concept_properties = {}
        for c in main_concepts:
            parent_props = handle_properties(c)
            for sc in sub_concepts.get(c, []):
                child_props = []
                props = handle_properties(sc, **parent_props.inheritable_props())
                if not parent_props.permit_attributes:
                    assert not props.permit_attributes
                    props.permit_attributes = False
                child_props.append(props)
                assert all(parent_props.typing_concept == props.typing_concept for props in child_props)

        return MITMDefinition(main_concepts=main_concepts, weak_concepts=self.weak_concepts, sub_concepts=sub_concepts,
                              concept_relations=concept_relations, concept_properties=concept_properties)
