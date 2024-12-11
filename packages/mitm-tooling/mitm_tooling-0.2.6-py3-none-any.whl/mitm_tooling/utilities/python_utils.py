from collections.abc import Sequence, Mapping
from typing import TypeVar, Hashable, Iterable, Callable, Any


def i_th(i: int, result_constr: type | None = tuple):
    if result_constr:
        return lambda t: result_constr(map(lambda x: x[i], t))
    else:
        return lambda t: map(lambda x: x[i], t)


K = TypeVar('K', bound=Hashable)
T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')


def ident(arg: T) -> T:
    return arg


def normalize_into_dict(arg: Iterable | dict) -> dict:
    return arg if isinstance(arg, dict) else {r: r for r in arg}


def unpack_singleton(arg: dict[K, T]) -> tuple[K, T]:
    k, v = next(iter(arg.items()))
    return k, v


def unpack_inner(arg: Iterable[dict[K, T1]], transform: Callable[[T1], T2] = ident) -> list[tuple[K, T2]]:
    return [(k, transform(v)) for d in arg for k, v in d.items()]


def normalize_vals(arg: dict[K, list[T] | dict[T, T]]):
    return {k: normalize_into_dict(v) for k, v in arg.items()}


def map_vals(arg: dict[K, T1], func: Callable[[T1], T2]) -> dict[K, T2]:
    return {k: func(v) for k, v in arg.items()}


def normalize_list_of_mixed(arg: list[str | dict[str, Any]]) -> dict[str, Any]:
    res = {}
    for c in arg:
        if isinstance(c, str):
            res[c] = None
        elif isinstance(c, dict):
            k, v = next(iter(c.items()))
            res[k] = v
    return res


def combine_dicts(d1: dict, d2: dict, defaults: dict | None = None) -> dict:
    if defaults is None:
        defaults = {}
    res = dict(d1)
    for k, v in d2.items():
        if k not in res or v is not None:
            res[k] = v
        if res[k] is None:
            res[k] = defaults.get(k, None)
    return res


def elem_wise_eq(it1: Iterable, it2: Iterable) -> Iterable[bool]:
    return map(lambda elems: elems[0] == elems[1], zip(it1, it2))


def grouped(it: Iterable[tuple[K, T]]) -> dict[K, list[T]]:
    res = {}
    for k, v in it:
        if k not in res:
            res[k] = []
        res[k].append(v)
    return res


def inner_list_concat(d1: dict[K, list[Any]], d2: dict[K, list[Any]]) -> dict[K, list[Any]]:
    res = {k: list(vs) for k, vs in d1.items()}
    for k, vs in d2.items():
        if k not in res:
            res[k] = []
        res[k].extend(vs)
    return res


def pick_from_mapping(d: Mapping[K, T], keys: Sequence[K]) -> list[tuple[K, T]]:
    return [(k, d[k]) for k in keys]


class ExtraInfoExc(Exception):
    def __init__(self, msg=None):
        super().__init__()
        if msg is not None:
            self.add_note(msg)
