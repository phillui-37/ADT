from abc import abstractmethod
from typing import TypeVar, Generic, Callable
from .Applicative import Applicative

_T = TypeVar('_T')
_R = TypeVar('_R')


class Monad(Applicative[_T], Generic[_T]):
    @staticmethod
    def result(value: _T) -> 'Monad[_T]':
        return Monad.pure(value)

    @abstractmethod
    def bind(self, f: 'Callable[[_T], Monad[_R]]') -> 'Monad[_R]':
        pass
