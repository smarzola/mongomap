import pytest

from mongomap import *


@pytest.fixture(scope='module')
def schema():
    class ASchema(Schema):
        foo = Field(IntType)
        bar = Field(FloatType)

    return ASchema


@pytest.fixture(scope='module')
def nested_schema(schema):
    class BSchema(Schema):
        spam = Field(StringType)
        egg = Field(schema)

    return BSchema


def test_schema(schema):
    sch = schema({'foo': 1, 'bar': 2.3})
    assert sch._dirty
    assert sch.foo == 1
    assert sch.bar == 2.3


def test_explicit_field_names():
    class ASchema(Schema):
        foo = Field(IntType, name='bar')
    sch = ASchema(bar=1)
    assert isinstance(ASchema.foo, Field)
    assert sch.bar == 1
    with pytest.raises(AttributeError):
        sch.foo


def test_schema_drop_extra(schema):
    sch = schema(dict(spam=3))
    with pytest.raises(AttributeError):
        sch.spam


def test_schema_missing(schema):
    sch = schema(dict(spam=3))
    assert sch.foo is None


def test_schema_marshal(schema):
    sch_dct = {'foo': 1, 'bar': 2.3}
    sch = schema(sch_dct)
    assert sch_dct == sch.marshal()


def test_nested(nested_schema):
    sch_dct = {'spam': 'egg', 'egg': {'foo': 1, 'bar': 2.3}}
    sch = nested_schema(sch_dct)
    assert sch.egg.foo == 1


def test_nested_marshal(nested_schema):
    sch_dct = {'spam': 'egg', 'egg': {'foo': 1, 'bar': 2.3}}
    sch = nested_schema(sch_dct)
    assert sch_dct == sch.marshal()


def test_init_params(nested_schema):
    sch_dct = {'spam': 'egg', 'egg': {'foo': 1, 'bar': 2.3}}
    sch = nested_schema(**sch_dct)
    assert sch_dct == sch.marshal()


def test_empty_marshal(nested_schema):
    sch = nested_schema()
    assert sch.marshal() == {'spam': None,
                             'egg': {'bar': None,
                                     'foo': None}}


def test_attach_values_later(nested_schema):
    sch = nested_schema()
    sch.spam = 'egg'
    assert sch.marshal() == {'spam': 'egg',
                             'egg': {'bar': None,
                                     'foo': None}}


def test_attach_deep_values(nested_schema):
    sch = nested_schema()
    sch.egg.foo = 42
    assert sch.marshal() == {'spam': None,
                             'egg': {'bar': None,
                                     'foo': 42}}
