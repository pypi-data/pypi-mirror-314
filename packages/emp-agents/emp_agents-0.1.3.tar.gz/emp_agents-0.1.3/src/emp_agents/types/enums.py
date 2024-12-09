from enum import StrEnum


class OpenAIModelType(StrEnum):
    gpt3_5 = "gpt-3.5-turbo-0125"
    gpt3_5_turbo = "gpt-3.5-turbo"
    gpt4 = "gpt-4"
    gpt4_turbo = "gpt-4-turbo"
    gpt4o_mini = "gpt-4o-mini"  # 128_000 tokens
    gpt4o = "gpt-4o"
    gpt_o1_mini = "o1-mini"
    gpt_o1_preview = "o1-preview"


class AnthropicModelType(StrEnum):
    claude_3_5_sonnet = "claude-3-5-sonnet-20240620"
    claude_3_opus = "claude-3-opus-20240229"
    claude_3_sonnet = "claude-3-sonnet-20240229"
    claude_3_haiku = "claude-3-haiku-20240307"
    claude_2_1 = "claude-2.1"
    claude_2_0 = "claude-2.0"
    claude_instant_1_2 = "claude-instant-1.2"


class Role(StrEnum):
    system = "system"
    user = "user"
    assistant = "assistant"
    tool = "tool"


ModelType = AnthropicModelType | OpenAIModelType
