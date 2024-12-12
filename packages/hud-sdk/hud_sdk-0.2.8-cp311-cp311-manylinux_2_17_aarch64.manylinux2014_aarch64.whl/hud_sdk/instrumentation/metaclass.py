from typing import Any, Type, TypeVar

T = TypeVar("T")


def overrideclass(inherit_class: Type[T]) -> Type[type]:
    class OverrideclassMetaclass(type):
        def __instancecheck__(cls, instance: Any) -> bool:
            if isinstance(instance, inherit_class):
                return True
            return super().__instancecheck__(instance)

        def __subclasscheck__(cls, subclass: Any) -> bool:
            if issubclass(subclass, inherit_class):
                return True
            return super().__subclasscheck__(subclass)

    return OverrideclassMetaclass
