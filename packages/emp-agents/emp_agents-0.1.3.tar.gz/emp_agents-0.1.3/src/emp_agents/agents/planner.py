from pydantic import BaseModel, Field

from emp_agents.agents.base import AgentBase


class Task(BaseModel):
    title: str
    description: str


class TaskList(BaseModel):
    tasks: list[Task]


class Planner(AgentBase):
    prompt: str = Field(
        default="You are a strategic planner, providing insights and generating tasks for given subjects. You are a subject matter expert, whatever the task."
    )

    async def generate(self, subject: str) -> TaskList:
        """
        Generate a strategic plan based on the given subject.

        Args:
            subject (str): The subject for which to generate a plan.

        Returns:
            TaskList: A detailed TaskList object with a set of tasks.
        """
        response = await self.respond(
            f"Generate a strategic actionable set of task for: {subject}",
            response_format=TaskList,
        )
        return TaskList.model_validate_json(response)
