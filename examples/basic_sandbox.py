"""Create a Leap0 sandbox backend and run a shell command.

See LangChain Deep Agents sandboxes: https://docs.langchain.com/oss/python/deepagents/sandboxes

Requires ``LEAP0_API_KEY`` (see https://leap0.dev).

Run from the repository root::

    uv run python examples/basic_sandbox.py
"""

from __future__ import annotations

import os
import sys

from leap0 import Leap0Client

from langchain_leap0 import Leap0Sandbox


def main() -> int:
    """Create a sandbox, echo a greeting, print output and exit code."""
    if not os.environ.get("LEAP0_API_KEY"):
        print("Set LEAP0_API_KEY in your environment.", file=sys.stderr)
        return 1

    client = Leap0Client()
    sandbox = client.sandboxes.create()
    backend = Leap0Sandbox(client=client, sandbox=sandbox)
    try:
        result = backend.execute("echo 'Hello LangChain from Leap0.dev'")
        print(result.output.strip())
        print("exit_code:", result.exit_code)
    finally:
        try:
            client.sandboxes.delete(sandbox)
        finally:
            client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
