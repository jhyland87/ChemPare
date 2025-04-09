from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import NoReturn
from typing import Union


@dataclass(init=True, match_args=True, kw_only=True, eq=True, order=True, unsafe_hash=True)
class TypeVariant(Dict):

    _id: int = None
    """Index of the variant"""

    uuid: Union[str, int] = None
    """Unique identifier used by supplier"""

    foo: str = None

    title: str = None
    """Title of the product"""

    name: str = None
    """Product name (sometimes different than title)"""

    description: str = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__super_keys = list(super().keys())
        self.__orig_args = kwargs
        self._keys = [key for key in self.__super_keys if str(key).startswith('_') is False]

    def __eq__(self, other):
        if not isinstance(other, TypeVariant):
            return False

        return str(dict(self).items()) == str(dict(other).items())

    def __repr__(self):
        args = [f"{k}='{v}'" for k, v in dict(self).items()]
        klass = type(self).__name__
        return f"{klass}({', '.join(args)})"

    def __str__(self):
        return str(dict(self))

    @property
    def _id(self):
        return self.__orig_args['_id']

    def keys(self):
        return self._keys

    def __iter__(self):
        """Used when dict(variant) is called. This will exclude empty values
        and private properties.
        """
        combined_data = list(super().__iter__()) + list(self.__dict__)
        return iter(combined_data)

    def items(self) -> List:
        """Get Variant dictionary items in list format"""
        return dict(self).items()

    def update(self, data: Dict) -> NoReturn:
        """Update the TypeProduct instance

        Args:
            data (Dict): Dictionary to merge into current dictioary
        """
        if not data or not isinstance(data, Dict):
            return

        for k, v in data.items():
            self[k] = v
            self._keys.append(k)


my_type = TypeVariant(_id=123, uuid="1234asbc", title="some title", name="some name")


def _print(*args):
    # print('{:>20}'.format('--------------------'))
    print('\n{:>30} : {:10}'.format(*args))


_print('hash1', str(my_type.__hash__))
my_type.update(dict(foo="bar"))
_print('hash2', str(my_type.__hash__))
_print('str(my_type)', str(my_type))
_print('my_type.__repr__()', str(my_type.__repr__()))
_print('dict(my_type)', str(dict(my_type)))
_print('my_type.__dict__', str(my_type.__dict__))
_print('my_type.items()', str(my_type.items()))
_print('my_type.get(uuid)', str(my_type.get("uuid")))
_print('iter(my_type)', str(iter(my_type)))

for k, v in my_type.items():
    _print(f"my_type[{k}]", v)


type_a = TypeVariant(uuid="foo")
type_b = TypeVariant(uuid="bar")
type_c = TypeVariant(uuid="foo")

_print("type_a", str(type_a))
_print("type_b", str(type_b))
_print("type_c", str(type_c))
_print("type_a == type_b", str(type_a == type_b))
_print("type_a == type_c", str(type_a == type_c))
