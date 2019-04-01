from abc import abstractmethod
from typing import TypeVar, Callable, Generic

_T = TypeVar('_T')
_R = TypeVar('_R')


class Functor(Generic[_T]):
    @abstractmethod
    def fmap(self, f: Callable[[_T], _R]) -> 'Functor[_R]':
        pass
