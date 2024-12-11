from collections.abc import Iterable
from typing import TypeVar, TypedDict, Callable, Generic, Literal, overload

from . import MITMDefinition
from .registry import get_mitm_def
from .definition_representation import COLUMN_GROUPS, ConceptKind, ConceptLevel, ConceptName, MITM
from mitm_tooling.utilities.python_utils import elem_wise_eq

T = TypeVar('T')


def dummy(): return None


def dummy_list(): return []


Mapper = Callable[[], T | tuple[str, T]]
MultiMapper = Callable[[], list[T] | Iterable[tuple[str, T]]]


class ColGroupMaps(TypedDict, Generic[T], total=False):
    kind: Mapper | None
    type: Mapper | None
    identity: MultiMapper | None
    inline: MultiMapper | None
    foreign: MultiMapper | None
    attributes: MultiMapper | None


def map_col_groups(mitm_def: MITMDefinition, concept: ConceptName, col_group_maps: ColGroupMaps[T],
                   ensure_unique: bool = True) -> \
        tuple[
            list[T], dict[str, T]]:
    concept_properties = mitm_def.get_properties(concept)

    created_results = {}
    results = []

    def add_results(cols: Iterable[T | tuple[str, T]]):
        for item in cols:
            if isinstance(item, tuple):
                name, result = item
            else:
                result = item
                name = str(item)
            if result is not None and (not ensure_unique or name not in created_results):
                created_results[name] = result
                results.append(result)

    for column_group in concept_properties.column_group_ordering:
        match column_group:
            case 'kind' if any(elem_wise_eq(concept_properties.nature, (ConceptLevel.Sub, ConceptKind.Abstract))):
                add_results([col_group_maps.get('kind', dummy)()])
            case 'type':
                add_results([col_group_maps.get('type', dummy)()])
            case 'identity-relations':
                add_results(col_group_maps.get('identity', dummy_list)())
            case 'inline-relations':
                add_results(col_group_maps.get('inline', dummy_list)())
            case 'foreign-relations':
                add_results(col_group_maps.get('foreign', dummy_list)())
            case 'attributes' if concept_properties.permit_attributes:
                add_results(col_group_maps.get('attributes', dummy_list)())

    return results, created_results
