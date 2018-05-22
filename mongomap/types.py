__all__ = ['IntType', 'FloatType', 'StringType', 'ByteType', 'DictType']


class BaseType:

    def __init__(self, value, allow_empty=True):
        super().__init__()
        self.value = self.validate(value, allow_empty)

    def validate(self, value, allow_empty=True):
        raise NotImplementedError  # pragma: no cover

    def marshal(self):
        raise NotImplementedError  # pragma: no cover


class PyMongoType(BaseType):
    typ = None

    def validate(self, value, allow_empty=True):
        if not value and allow_empty:
            return value
        if not isinstance(value, self.typ):
            raise TypeError
        return value

    def marshal(self):
        return self.value


class IntType(PyMongoType):
    typ = int


class FloatType(PyMongoType):
    typ = float


class StringType(PyMongoType):
    typ = str


class ByteType(PyMongoType):
    typ = bytes


class DictType(PyMongoType):
    typ = dict
