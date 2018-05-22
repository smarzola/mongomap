from mongomap.fields import Field
from mongomap.types import BaseType


class ChangeTracker:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._changes = set()

    @property
    def _dirty(self):
        return bool(self._changes)

    def _changed(self, field):
        self._changes.add(field)


class SchemaMeta(type):
    def __new__(mcs, name, bases, classdct):
        fields = []

        for attrname, cls_attr in classdct.items():
            if isinstance(cls_attr, Field):
                if cls_attr.name is None:
                    cls_attr.name = attrname
                fields.append(cls_attr.name)

        classdct['_fields'] = tuple(fields)

        return super().__new__(mcs, name, bases, classdct)


class Schema(ChangeTracker, BaseType, metaclass=SchemaMeta):

    def __init__(self, dct=None, **kwargs):
        if dct is None:
            dct = kwargs
        super().__init__(dct)
        for field in self._fields:
            setattr(self, field, dct.get(field))

    def validate(self, value, allow_empty=True):
        return self

    def marshal(self):
        return {
            field: self.__class__.__dict__.get(field).marshal(self)
            for field in self._fields
        }
