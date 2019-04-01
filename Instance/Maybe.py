from abc import abstractmethod
from typing import TypeVar, Generic, Callable

from ..TypeClass.Monad import Monad

_T = TypeVar('_T')
_R = TypeVar('_R')
_E = TypeVar('_E')


class Maybe(
    Monad[_T],
    Generic[_T]
):
    """
    Only filter None, for other please use filter/map
    """

    def __init__(self, *args, **kwargs):
        raise TypeError('Cannot get Option object directly, use function "of"')

    @staticmethod
    def of(value: _T) -> 'Maybe[_T]':
        if value is None:
            return Nothing()
        return Just(value)

    @property
    @abstractmethod
    def is_just(self) -> bool:
        pass

    @property
    def is_nothing(self) -> bool:
        return not self.is_just

    @staticmethod
    def pure(value: _T) -> 'Maybe[_T]':
        return Maybe.of(value)

    def unwrap(self) -> _T:
        """
        Just -> return value
        Nothing -> raise ValueError
        """
        if self.is_nothing:
            raise ValueError("This is Nothing")
        return self._value

    def unwrap_or(self, default: _T) -> _T:
        """
        Just -> return value
        Nothing  -> return default
        """
        try:
            return self.unwrap()
        except ValueError:
            return default

    def unwrap_or_else(self, default_f: Callable[[], _T]) -> _T:
        try:
            return self.unwrap()
        except ValueError:
            return default_f()

    def fmap_or(self, default: _R, f: Callable[[_T], _R]) -> _R:
        return default if self.is_nothing else f(self._value)

    def fmap_or_else(self, default_f: Callable[[], _R], f: Callable[[_T], _R]) -> _R:
        return default_f() if self.is_nothing else f(self._value)

    def ok_or(self, err: Exception) -> 'Either[_T, _E]':
        from ADTV2.Instance.Either import Either
        return Either.of(self._value if self.is_just else err)

    def ok_or_else(self, err_f: Callable[[], Exception]) -> 'Either[_T, _E]':
        from ADTV2.Instance.Either import Either
        return Either.of(self._value if self.is_just else err_f())

    def filter(self, f: Callable[[_T], bool]) -> 'Maybe[_T]':
        if self.is_nothing:
            return Nothing()
        return Nothing() if not f(self._value) else Just(f)

    def or_(self, value: 'Maybe[_T]') -> 'Maybe[_T]':
        if self.is_just:
            return self
        return value

    def or_else(self, value_f: Callable[[], 'Maybe[_T]']) -> 'Maybe[_T]':
        if self.is_just:
            return self
        return value_f()

    def and_(self, value: 'Maybe[_T]') -> 'Maybe[_T]':
        if self.is_nothing:
            return self
        return value

    def and_then(self, value_f: 'Callable[[_T], Maybe[_R]]') -> 'Maybe[_R]':
        return self.bind(value_f)

    def xor(self, value: 'Maybe[_T]') -> 'Maybe[_T]':
        if (self.is_just and value.is_just) or (self.is_nothing and value.is_nothing):
            return Nothing()
        return self if self.is_just else value


class Just(Maybe[_T], Generic[_T]):
    def __init__(self, value: _T):
        self._value = value

    @property
    def is_just(self) -> bool:
        return True

    def fmap(self, f: Callable[[_T], _R]) -> Maybe[_R]:
        return Maybe.of(f(self._value))

    def bind(self, f: 'Callable[[_T], Maybe[_R]]') -> 'Maybe[_R]':
        return f(self._value)

    def combine(self, value: 'Maybe[_T]') -> 'Maybe[_R]':
        """
        can only be use when Just.value is callable
        """
        return value.fmap(self._value)


class Nothing(Maybe[None]):
    def __init__(self):
        pass

    @property
    def is_just(self) -> bool:
        return False

    def fmap(self, f: Callable[[_T], _R]) -> Maybe[None]:
        return self

    def bind(self, f: 'Callable[[_T], Maybe[_R]]') -> 'Maybe[None]':
        return self

    def combine(self, value: 'Maybe[_T]') -> 'Maybe[_R]':
        return self


if __name__ == '__main__':
    print(Maybe.of(None).fmap(lambda x: x + 1))
    print(Maybe.of(''))
    print(Maybe.of(1).bind(lambda x: Maybe.of(x+1)).bind(lambda _: Maybe.of(None)))
    print(Maybe.of([]))
    try:
        print(Maybe())
    except TypeError:
        print('fail 1')
    try:
        print(Maybe(1))
    except TypeError:
        print('fail 2')


    def half(x):
        print(x)
        if x & 1 == 1:
            return Maybe.of(None)
        return Maybe.of(x//2)

    print(Maybe.of(20).bind(half).bind(half).bind(half))