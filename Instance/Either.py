from abc import abstractmethod
from typing import TypeVar, Generic, Callable

from ..TypeClass.Monad import Monad

_T = TypeVar('_T')
_R = TypeVar('_R')
_E = TypeVar('_E')


class Either(
    Monad[_T],
    Generic[_T, _E]
):
    def __init__(self, *args, **kwargs):
        raise TypeError('Cannot get Either object directly, use function "of"')

    @staticmethod
    def of(value: _T) -> 'Either[_T, _E]':
        """
        err/exception -> Left
        normal -> right
        """
        if isinstance(value, Exception):
            return Left(value)
        return Right(value)

    @property
    @abstractmethod
    def is_left(self) -> bool:
        pass

    @property
    def is_right(self) -> bool:
        return not self.is_left

    @staticmethod
    def pure(value: _T) -> 'Either[_T, _E]':
        return Either.of(value)

    def unwrap(self) -> _T:
        if self.is_left:
            raise self._err from self._err
        return self._value

    def unwrap_or(self, default: _T) -> _T:
        if self.is_right:
            return self._value
        return default

    def unwrap_or_else(self, default_f: Callable[[], _T]) -> _T:
        if self.is_right:
            return self._value
        return default_f()

    def fmap_or(self, default: _R, f: Callable[[_T], _R]) -> _R:
        return default if self.is_left else f(self._value)

    def fmap_or_else(self, default_f: Callable[[], _R], f: Callable[[_T], _R]) -> _R:
        return default_f() if self.is_left else f(self._value)

    def or_(self, value: 'Either[_T, _E]') -> 'Either[_T, _E]':
        return self if self.is_right else value

    def or_else(self, value_f: Callable[[], 'Either[_T, _E]']) -> 'Either[_T, _E]':
        return self if self.is_right else value_f()

    def and_(self, value: 'Either[_T, _E]') -> 'Either[_T, _E]':
        if self.is_left:
            return self
        return value

    def and_then(self, value_f: 'Callable[[_T], Either[_T, _E]]') -> 'Either[_T, _E]':
        return self.bind(value_f)

    def expect(self, msg: str) -> _T:
        if self.is_left:
            raise ValueError(msg)
        return self._value

    def unwrap_left(self) -> _E:
        if self.is_right:
            raise ValueError('This is Right that cannot invoke "unwrap_left"')
        return self._err

    def expect_err(self, msg: str) -> _E:
        if self.is_right:
            raise ValueError(msg)
        return self._err

class Left(Either[_T, _E], Generic[_T, _E]):
    def __init__(self, err: _E):
        self._err = err

    @property
    def is_left(self) -> bool:
        return True

    def bind(self, f: 'Callable[[_T], Either[_R, _E]]') -> Either[_R, _E]:
        return self

    def combine(self, value: Either[_T, _E]) -> Either[_R, _E]:
        return self

    def fmap(self, f: Callable[[_T], _R]) -> Either[_R, _E]:
        return self


class Right(Either[_T, _E], Generic[_T, _E]):
    def __init__(self, value: _T):
        self._value = value

    @property
    def is_left(self) -> bool:
        return False

    def bind(self, f: 'Callable[[_T], Either[_R, _E]]') -> 'Either[_R, _E]':
        return f(self._value)

    def combine(self, value: 'Either[_T, _E]') -> 'Either[_R, _E]':
        return value.fmap(self._value)

    def fmap(self, f: Callable[[_T], _R]) -> 'Either[_R, _E]':
        return Either.of(f(self._value))


