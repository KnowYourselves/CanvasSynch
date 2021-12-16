from typing import Any, Dict, TypeVar, Type
import inspect

T = TypeVar("T", bound="BaseClass")


class BaseClass:
    def __init__(*args):
        pass

    @classmethod
    def from_dict(cls: Type[T], _dict: Dict[str, Any]) -> T:
        return cls(
            **{k: v for k, v in _dict.items() if k in inspect.signature(cls).parameters}
        )

    def to_dict(self):
        return self.__dict__
