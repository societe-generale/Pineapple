import pytest

from pineapple_core.core.types import PineappleType, Any


def test_that_pineapple_type_is_abstract():
    with pytest.raises(NotImplementedError):
        PineappleType().check(22)


def test_that_pineapple_type_is_printable():
    assert Any().__repr__() == "Any"
