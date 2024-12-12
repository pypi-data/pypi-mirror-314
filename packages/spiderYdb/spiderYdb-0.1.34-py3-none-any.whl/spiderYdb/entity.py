from .entityMeta import EntityMeta
from .fields import Field
from .query import Query


class Entity(object, metaclass=EntityMeta):
    def __init__(self, *args, new=True, **kwargs):
        if args:
            raise TypeError('%s constructor accept only keyword arguments. Got: %d positional argument%s'
                                 % (self.__name__, len(args), len(args) > 1 and 's' or ''))
        self.params = dict()
        for atr in self.attrs_dict:
            attr = self.attrs_dict[atr].copy()
            if atr in kwargs:
                # if atr == 'id':
                    # print(atr, kwargs[atr], type(attr))
                attr.changed = new
                attr.set_value(kwargs[atr])
            self.params[atr] = attr
        self._database_.add_item(self)

    @property
    def fields(self):
        return self.__dict__.items()

    @property
    def need_update(self):
        for field in self.params:
            if self.params[field].changed:
                return True

    def save(self):
        return Query.save_item(self)

    @classmethod
    def from_dict(cls, obj):
        return cls(new=False, **obj)

    def __getattribute__(self, item):
        field = object.__getattribute__(self, item)
        if isinstance(field, Field):
            return self.params[field.name].value
        return field

    def __setattr__(self, key, value):
        if key in self.attrs_dict:
            field = self.params[key]
            field.value = value
            field.changed = True
        else:
            self.__dict__[key] = value

    def __str__(self):
        result = [f'{self.__class__.__name__} table {self.table_name}']
        for field in self.params:
            field = self.params[field].value
            if str(field):
                result.append(str(field))
        return str('\n'.join(result))


    def object(self):
        result = {}
        for field in self.params:
            result[field] = self.params[field].value
        return result