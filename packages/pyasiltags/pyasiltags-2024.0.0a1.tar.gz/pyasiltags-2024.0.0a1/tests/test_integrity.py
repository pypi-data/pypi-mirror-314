import pytest

from pyasiltags import validate
from pyasiltags import Integrity
from pyasiltags import IntegrityError

valid_asil = [
    " ASIL_D ",
    " ASIL_D (QM )",
    " ASIL_D",
    " AsilD ",
    " ASILD ( a )",
    " ASILD ( B )",
    "ASIL A",
    "ASIL_D",
    "ASIL-C",
    "ASILB",
    "ASILD(QM)",
    "qm (b )",
    "qm",
    "QM",
    "QM(B)",
]

invalid_asil = [
    "a",
    "ASIL QM",
    "ASIL-A( E)",
    "ASIL-E",
    "ASIL-E",
    "asilad",
    "ASILE",
    "asilqm",
    "bob",
]


@pytest.mark.parametrize("input", valid_asil)
def test_exception_valid_asil(input):
    Integrity(input)


@pytest.mark.parametrize("input", invalid_asil)
def test_exception_invalid_asil(input):
    with pytest.raises(IntegrityError):
        Integrity(input)


@pytest.mark.parametrize("input", valid_asil)
def test_valid_asil(input):
    assert validate(input)


@pytest.mark.parametrize("input", invalid_asil)
def test_invalid_asil(input):
    assert not validate(input)
