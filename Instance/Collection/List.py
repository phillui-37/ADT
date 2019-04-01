from functools import reduce
from typing import TypeVar, Generic, Callable, Iterable, Optional, Iterator, Union, Any

import FP

from ..Maybe import Maybe
from ...TypeClass.Monad import Monad

_T = TypeVar('_T')
_R = TypeVar('_R')


class List(
    Monad[_T],
    Generic[_T]
):
    def __init__(self, iterable: Optional[Iterable[_T]] = None):
        if iterable is not None and isinstance(iterable, List):
            self.data = iterable.data
        else:
            self.data = list(iterable) or []

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> 'Iterable[_T]':
        self.__idx = 0
        return self

    def __next__(self) -> _T:
        if self.__idx < len(self.data):
            ret = self.data[self.__idx]
            self.__idx += 1
            return ret
        else:
            raise StopIteration()

    def __str__(self) -> str:
        return str(self.data)

    def copy(self) -> 'List[_T]':
        return List(self.data.copy())

    def append(self, obj: _T) -> 'List[_T]':
        return List(self.data + [obj])

    def extend(self, iterable: Iterable[_T]) -> 'List[_T]':
        return List(self.data + list(iterable))

    def index(self, obj: _T, start: Optional[int] = None, stop: Optional[int] = None) -> Maybe[int]:
        try:
            return Maybe.of(self.data.index(obj, start, stop))
        except ValueError:
            return Maybe.of(None)

    def count(self, obj: _T) -> int:
        return self.data.count(obj)

    def insert(self, index: int, object: _T) -> 'List[_T]':
        return List(self.data[:index] + [object] + self.data[index:])

    def remove(self, object: _T) -> 'List[_T]':
        return List(filter(lambda x: x != object, self.data))

    def reverse(self) -> 'List[_T]':
        return List(reversed(self.data))

    def sort(self, key: Optional[Callable[[_T], Any]] = None, reverse: bool = False) -> 'List[_T]':
        return List(sorted(self.data, key=key, reverse=reverse))

    def __getitem__(self, i: Union[int, slice]) -> Maybe[Union[_T, 'List[_T]']]:
        try:
            return Maybe.of(self.data[i])
        except IndexError:
            return Maybe.of(None)

    def __setitem__(self, i: int, o: _T):
        """
        This is impure
        """
        self.data[i] = o

    def __delitem__(self, i: Union[int, slice]):
        """
        This is impure
        """
        self.data.__delitem__(i)

    def __add__(self, x: 'List[_T]') -> 'List[_T]':
        return List(self.data + x.data)

    def __iadd__(self, x: 'List[_T]') -> 'List[_T]':
        return List(self.data + x.data)

    def __mul__(self, n: int) -> 'List[_T]':
        return List(x*n for x in self.data)

    def __rmul__(self, n: int) -> 'List[_T]':
        return List(x*n for x in self.data)

    def __imul__(self, n: int) -> 'List[_T]':
        return List(x*n for x in self.data)

    def __contains__(self, o: _T) -> bool:
        return self.data.__contains__(o)

    def __reversed__(self) -> Iterator[_T]:
        return reversed(self.data)

    def __gt__(self, x: 'List[_T]') -> bool:
        return self.data > x.data

    def __ge__(self, x: 'List[_T]') -> bool:
        return self.data >= x.data

    def __lt__(self, x: 'List[_T]') -> bool:
        return self.data < x.data

    def __le__(self, x: 'List[_T]') -> bool:
        return self.data <= x.data

    @property
    def is_empty(self) -> bool:
        return len(self) == 0

    def bind(self, f: 'Callable[[_T], List[_R]]') -> 'List[_R]':
        return List(FP.concat(map(f, self.data)))

    @staticmethod
    def pure(value: _T) -> 'List[_T]':
        return List([value])

    def combine(self, value: 'List[_T]') -> 'List[_R]':
        return List(reduce(lambda x, y: x(y), zip(self, value)))

    def fmap(self, f: Callable[[_T], _R]) -> 'List[_R]':
        return List(f(x) for x in self)

