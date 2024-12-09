from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Generic, TypeVar

if TYPE_CHECKING:
    from emp_agents.models.shared import Request


T = TypeVar("T")


class TCompletionAgent(ABC, Generic[T]):

    @abstractmethod
    async def completion(self, req: "Request") -> T: ...
