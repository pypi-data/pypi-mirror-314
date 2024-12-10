from typing import Any, Dict, Tuple, Type, TypeVar

T = TypeVar("T")


class OverrideclassMetaclass(type):
    def __new__(
        cls, name: str, bases: Tuple[Any, ...], dct: Dict[Any, Any], **kwargs: Any
    ) -> Any:
        return super().__new__(cls, name, bases, dct)

    def __init__(
        cls,
        name: str,
        bases: Tuple[Any, ...],
        dct: Dict[Any, Any],
        inherit_class: Type[T],
        **kwargs: Any
    ) -> None:
        cls._inherit_class = inherit_class
        super().__init__(name, bases, dct, **kwargs)

    def __instancecheck__(cls, instance: Any) -> bool:
        if isinstance(instance, cls._inherit_class):
            return True
        return super().__instancecheck__(instance)

    def __subclasscheck__(cls, subclass: Any) -> bool:
        if issubclass(subclass, cls._inherit_class):
            return True
        return super().__subclasscheck__(subclass)
