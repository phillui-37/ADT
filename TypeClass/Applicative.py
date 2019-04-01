from abc import abstractmethod
from typing import TypeVar, Generic

from .Functor import Functor

_T = TypeVar('_T')
_R = TypeVar('_R')


class Applicative(Functor[_T], Generic[_T]):
    @staticmethod
    @abstractmethod
    def pure(value: _T) -> 'Applicative[_T]':
        pass

    @abstractmethod
    def combine(self, value: 'Applicative[_T]') -> 'Applicative[_R]':
        pass
