from typing import ClassVar

import httpx
from pydantic import BaseModel

from emp_agents.models.openai.request import Message, Tool
from emp_agents.models.openai.response import Response
from emp_agents.models.openai.tool import Function, Parameters, Property
from emp_agents.models.openai.types import Classification
from emp_agents.models.shared import Request
from emp_agents.types import TCompletionAgent


class OpenAIBase(BaseModel, TCompletionAgent[Response]):
    URL: ClassVar[str] = "https://api.openai.com/v1/chat/completions"
    openai_api_key: str

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.openai_api_key}",
        }

    async def completion(self, request: Request) -> Response:
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.post(
                self.URL, json=request.to_openai(), timeout=None
            )
        if response.status_code >= 400:
            raise ValueError(response.json())
        return Response(**response.json())


__all__ = [
    "Classification",
    "Message",
    "OpenAIBase",
    "Request",
    "Response",
    "Tool",
    "Function",
    "Property",
    "Parameters",
]
