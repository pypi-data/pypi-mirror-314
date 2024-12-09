from collections.abc import Callable
from typing import Any


class ImplicitManager:
    implicits: dict[str, Any] = {}

    @classmethod
    def get_implicit(cls, name: str):
        """Get an implicit argument by name"""
        if name not in cls.implicits:
            raise ValueError(f"Implicit {name} not found")
        return cls.implicits[name]

    @classmethod
    def add_implicit(cls, name: str, implicit: Any):
        """Adds a new implicit argument"""
        cls.implicits[name] = implicit

    @classmethod
    def lazy_implicit(cls, name: str) -> Callable[..., Any] | Any:
        """Create a lazy implicit that can be resolved later"""

        def _get_implicit(*args, **kwargs) -> Any:
            imp = cls.get_implicit(name)
            if callable(imp):
                return imp(*args, **kwargs)
            return imp

        return _get_implicit
