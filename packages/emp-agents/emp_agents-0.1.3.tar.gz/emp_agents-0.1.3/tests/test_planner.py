import os

import pytest

from emp_agents.agents.planner import Planner, Task, TaskList
from emp_agents.types import OpenAIModelType


@pytest.mark.asyncio(scope="session")
async def test_generate():
    agent = Planner(
        default_model=OpenAIModelType.gpt4o_mini,
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
    )
    subject = "write a blog post"
    task_list = await agent.generate(subject)
    assert isinstance(task_list, TaskList)

    assert len(task_list.tasks) > 0

    for task in task_list.tasks:
        assert isinstance(task, Task)
        assert isinstance(task.title, str)
        assert isinstance(task.description, str)
        assert task.title != ""
        assert task.description != ""
