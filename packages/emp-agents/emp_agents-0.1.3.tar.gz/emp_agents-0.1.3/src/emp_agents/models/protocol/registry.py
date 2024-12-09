from typing import ClassVar

from emp_agents.models import GenericTool


class ToolRegistry:
    """Registry to store tool class and method information."""

    _registry: ClassVar[dict[str, type]] = {}

    @classmethod
    def register_class(cls, tool_class: type) -> None:
        """Register a tool class and collect its decorated methods."""
        class_name = tool_class.__name__
        cls._registry[class_name] = tool_class

    @classmethod
    def get_tool(cls, skill_name: str, tool_name: str) -> GenericTool:
        return cls._registry[skill_name]._tools_map[tool_name]

    @classmethod
    def get_skill(cls, skill_name: str) -> list[GenericTool]:
        return cls._registry[skill_name]._tools
