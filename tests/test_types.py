from collections import namedtuple

import pytest

from mongomap.types import *


@pytest.fixture(scope='module')
def pymongo_cases():
    PyMongoCase = namedtuple('PyMongoCase', 'klass valid invalid')
    cases = (
        PyMongoCase(IntType, 42, 'foo'),
        PyMongoCase(FloatType, 7.5, 42),
        PyMongoCase(StringType, 'foo', 7.5),
        PyMongoCase(ByteType, b'bar', 'foo')
    )
    return cases


def test_int(pymongo_cases):
    for case in pymongo_cases:
        typ = case.klass(case.valid)
        assert typ.marshal() == case.valid
        with pytest.raises(TypeError):
            case.klass(case.invalid)
