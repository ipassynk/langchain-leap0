"""Use ``Leap0Sandbox`` as the Deep Agents backend (shell + files).

Uses OpenAI chat models via ``create_deep_agent(model="openai:...")``.

See LangChain Deep Agents sandboxes: https://docs.langchain.com/oss/python/deepagents/sandboxes

Environment:

- ``LEAP0_API_KEY`` — Leap0 API key (https://leap0.dev).
- ``OPENAI_API_KEY`` — OpenAI API key.
- ``OPENAI_MODEL`` — optional, default ``openai:gpt-4o`` (any ``init_chat_model`` spec).

Run from the repository root::

    uv run python examples/deep_agent_sandbox.py
"""

from __future__ import annotations

import os
import sys

from deepagents import create_deep_agent
from leap0 import Leap0Client

from langchain_leap0 import Leap0Sandbox

_DEFAULT_OPENAI_MODEL = "openai:gpt-4o"


def main() -> int:
    """Run Deep Agent with Leap0 backend; create a script and run it in the sandbox."""
    if not os.environ.get("LEAP0_API_KEY"):
        print("Set LEAP0_API_KEY in your environment.", file=sys.stderr)
        return 1
    if not os.environ.get("OPENAI_API_KEY"):
        print("Set OPENAI_API_KEY in your environment.", file=sys.stderr)
        return 1

    model = os.environ.get("OPENAI_MODEL", _DEFAULT_OPENAI_MODEL).strip()

    client = Leap0Client()
    sandbox = client.sandboxes.create()
    backend = Leap0Sandbox(client=client, sandbox=sandbox)
    try:
        agent = create_deep_agent(
            model=model,
            system_prompt="You are a coding assistant with sandbox access.",
            backend=backend,
        )
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Create a hello world Python script and run it",
                    },
                ],
            },
        )
        print(result)
    finally:
        try:
            client.sandboxes.delete(sandbox)
        finally:
            client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
