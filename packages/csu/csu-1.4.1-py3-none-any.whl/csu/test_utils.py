import pytest

from .utils import singleton_memoize
from .utils import singleton_property


def test_singleton_memoize():
    pytest.raises(TypeError, singleton_memoize, lambda a: 123)
    a = []

    @singleton_memoize
    def stuff1(x=2):
        a.append(1)
        return "abc"

    assert a == []
    assert stuff1() == "abc"
    assert stuff1() == "abc"
    assert a == [1]

    b = []

    @singleton_memoize
    def stuff2():
        b.append(1)
        return "bce"

    assert b == []
    assert stuff2() == "bce"
    assert stuff2() == "bce"
    assert b == [1]


def test_singleton_property():
    c = []

    class Stuff3:
        @singleton_property
        def stuff():
            c.append(1)
            return "asd"

    assert c == []
    assert Stuff3().stuff == "asd"
    assert Stuff3().stuff == "asd"
    assert c == [1]

    d = []

    class Stuff4:
        @singleton_property
        @staticmethod
        def stuff():
            d.append(1)
            return "qwe"

    assert d == []
    assert Stuff4().stuff == "qwe"
    assert Stuff4().stuff == "qwe"
    assert d == [1]
