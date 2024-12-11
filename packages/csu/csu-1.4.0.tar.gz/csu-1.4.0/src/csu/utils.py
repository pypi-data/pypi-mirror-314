from collections.abc import Callable
from decimal import Decimal
from inspect import Parameter
from inspect import signature
from typing import TypeVar

ZERO = Decimal(0)
DOT01 = Decimal("0.01")
DOT001 = Decimal("0.001")
DOT0001 = Decimal("0.0001")
ONE00 = Decimal("100.0")


def validate_no_required_arguments(func):
    if isinstance(func, staticmethod):
        func = func.__func__
    required = [param for param in signature(func).parameters.values() if param.default is Parameter.empty]
    if required:
        raise TypeError(f"{func} cannot have mandatory arguments: {required}")


_T = TypeVar("_T")


def singleton_memoize(func: Callable[[], _T]) -> _T:
    validate_no_required_arguments(func)

    unset = object()

    class Singleton:
        value = unset

        def __get__(self, instance, owner):
            return self

        def __call__(self):
            if self.value is unset:
                value = self.value = func()
            else:
                value = self.value
            return value

    return Singleton()


def singleton_property(func: Callable[[], _T]) -> _T:
    if isinstance(func, staticmethod):
        func = func.__func__
    validate_no_required_arguments(func)

    unset = object()

    class Singleton:
        value = unset

        def __get__(self, instance, owner):
            if self.value is unset:
                value = self.value = func()
            else:
                value = self.value
            return value

    return Singleton()
