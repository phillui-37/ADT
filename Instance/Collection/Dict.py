from typing import TypeVar, Generic, Iterator, Iterable, ItemsView, ValuesView, KeysView, Mapping, Tuple, Optional, \
    Union, Callable

from ..Maybe import Maybe
from ...TypeClass.Functor import Functor

_K = TypeVar('_K')
_V = TypeVar('_V')
_R = TypeVar('_R')


class Dict(
    Functor[Tuple[_K, _V]],
    Generic[_K, _V]
):
    def __init__(self, value: Optional[dict] = None, **kwargs):
        self.data = {
            **(value or {}),
            **kwargs
        }

    def copy(self) -> 'Dict[_K, _V]':
        return Dict(self.data.copy())

    def update(self, m: Union[Mapping[_K, _V], Iterable[Tuple[_K, _V]]], **kwargs: _V) -> 'Dict[_K, _V]':
        if not isinstance(m, dict):
            m = dict(m)
        # TODO should be done by share path... well
        return Dict(**self.data, **m, **kwargs)

    def keys(self) -> KeysView[_K]:
        return self.data.keys()

    def values(self) -> ValuesView[_V]:
        return self.data.values()

    def items(self) -> ItemsView[_K, _V]:
        return self.data.items()

    @staticmethod
    def fromkeys(seq: Iterable[_K], value: Optional[_V] = None) -> 'Dict[_K, Optional[_V]]':
        return Dict(dict.fromkeys(seq, value))

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, k: _K) -> Maybe[_V]:
        try:
            return Maybe.of(self.data[k])
        except KeyError:
            return Maybe.of(None)

    def __setitem__(self, k: _K, v: _V):
        self.data.__setitem__(k, v)

    def __delitem__(self, k: _K):
        self.data.__delitem__(k)

    def __iter__(self) -> Iterator[_K]:
        return iter(self.data)

    def __str__(self) -> str:
        return str(self.data)

    def get(self, k: _K) -> Maybe[_V]:
        return self.__getitem__(k)

    def fmap(self, f: Callable[[Tuple[_K, _V]], Tuple[_K, _R]]) -> 'Dict[_K, _R]':
        return Dict(dict(f((x, y)) for x, y in self.items()))

    def filter(self, f: Callable[[Tuple[_K, _V]], bool]) -> 'Dict[_K, _V]':
        return Dict(dict((x, y) for x, y in self.items() if f((x, y))))


if __name__ == '__main__':
    print(Dict(a=1, b=2).fmap(lambda x: (x[0], x[1] + 1)))
