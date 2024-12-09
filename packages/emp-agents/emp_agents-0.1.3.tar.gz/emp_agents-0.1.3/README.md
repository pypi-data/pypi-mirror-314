# emp-agents

A library for building low-code, capable and extensible autonomous agent systems open sourced by [Empyreal](https://empyrealsdk.com/).

---

## Docs

Read the docs [here](https://emp-agents.empyrealsdk.com/)

---

## Quick Start

```shell
pip install emp-agents
```

```python
import asyncio
import os

from eth_rpc import set_alchemy_key

from emp_agents.agents.skills import SkillsAgent
from emp_agents.tools.dexscreener import DexScreenerSkill
from emp_agents.tools.protocol.erc20 import ERC20Skill
from emp_agents.tools.protocol.wallets import SimpleWalletSkill
from emp_agents.types import OpenAIModelType

if alchemy_key := os.environ.get("ALCHEMY_KEY"):
    set_alchemy_key(alchemy_key)


agent = SkillsAgent(
    skills=[
        ERC20Skill,
        SimpleWalletSkill,
        DexScreenerSkill,
    ],
    default_model=OpenAIModelType.gpt_4o,
    openai_api_key=os.environ.get("OPENAI_API_KEY"),
)


if __name__ == "__main__":
    asyncio.run(agent.run())
```

## Available SkillSets

SkillSets are designed to extend the capabilities of the agent by providing a collection of tools that can be used to perform tasks. The following SkillSets are currently available

- [SimpleWalletSkill](https://github.com/empyrealapp/emp-agents/blob/main/src/emp_agents/tools/protocol/wallets/simple.py)
- [ERC20Skill](https://github.com/empyrealapp/emp-agents/blob/main/src/emp_agents/tools/protocol/erc20/__init__.py)
- [GmxSkill](https://github.com/empyrealapp/emp-agents/blob/main/src/emp_agents/tools/protocol/gmx/__init__.py)
- [TwitterSkill](https://github.com/empyrealapp/emp-agents/blob/main/src/emp_agents/tools/twitter/__init__.py)
- [DexScreenerSkill](https://github.com/empyrealapp/emp-agents/blob/main/src/emp_agents/tools/dexscreener/__init__.py)

## Creating a Custom SkillSet

SkillsSets is a collection of tools that can be used to build agents. To create a custom SkillsSet, you can subclass the `SkillsSet` class and implement the `tools` property. SkillSets are designed to be modular and extensible and they are supported both by the OpenAI models and Anthropic models.

You can see an example of a custom SkillsSet in the [docs](./docs/agents.md).


## Future Work

Some of the features we are working on open sourcing are:

- Agent Autonomy
- Simulacrum SkillSet
- Agent Memory system
- Research SkillSets
- Prebuilt Agent Templates
- Pluggable library components

Reach out at [EmpyrealSDK](https://x.com/EmpyrealSDK) if you would like to learn more about the project.
