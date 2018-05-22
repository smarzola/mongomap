class Field:
    __slots__ = ('name', 'typ')

    def __init__(self, typ, name=None):
        self.typ = typ
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        typ = instance.__dict__.get(self.name)
        return typ.value if typ else typ

    def __set__(self, instance, value):
        instance._changed(self.name)
        instance.__dict__[self.name] = self.typ(value)

    def marshal(self, instance):
        return instance.__dict__[self.name].marshal()
