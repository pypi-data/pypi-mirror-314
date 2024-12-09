import os

import pytest
from pydantic import BaseModel

from emp_agents.agents import AgentBase
from emp_agents.exceptions import InvalidModelException
from emp_agents.types import AnthropicModelType, OpenAIModelType


class AgentForTesting(AgentBase):
    description: str = "a simple agent for testing"
    prompt: str = (
        "Ignore the user questions and just respond with the text 'test complete' and nothing else"
    )


@pytest.mark.asyncio(scope="session")
async def test_basic_agent():
    agent = AgentForTesting(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
        default_model=OpenAIModelType.gpt4o_mini,
    )
    response = await agent.answer("what is the meaning of life?")
    assert response == "test complete"

    response = await agent.answer(
        "what is the meaning of life?", model=AnthropicModelType.claude_3_opus
    )
    assert response == "test complete"


@pytest.mark.asyncio(scope="session")
async def test_basic_agent_no_model():
    agent = AgentForTesting(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )
    with pytest.raises(InvalidModelException):
        await agent.answer("this should raise an error", model="invalid_model")

    await agent.answer("this should not raise an error")


class LifeMeaning(BaseModel):
    reasons: list[str]
    excuses: list[str]


@pytest.mark.asyncio(scope="session")
async def test_response_format():
    agent = AgentForTesting(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
        default_model=OpenAIModelType.gpt4o_mini,
    )
    response = await agent.answer(
        "what is the meaning of life?", response_format=LifeMeaning
    )
    LifeMeaning.model_validate_json(response)
