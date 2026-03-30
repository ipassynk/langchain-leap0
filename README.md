# langchain-leap0

**Leap0** integration for [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/sandboxes): a `BaseSandbox` backend that runs shell commands and file transfers inside a Leap0 sandbox.

**[Leap0](https://leap0.dev)** is enterprise-grade cloud sandboxes for AI agents. Launch isolated sandboxes in ~200ms. Give every agent its own compute, filesystem, and network boundary while your agents run safely.

## Quick install

```bash
pip install langchain-leap0
```

Set your API key (see [Leap0](https://leap0.dev) for account and key management):

```bash
export LEAP0_API_KEY="your-key"
```

Minimal usage with the `[leap0](https://pypi.org/project/leap0/)` SDK and `Leap0Sandbox`:

```python
from leap0.client import Leap0Client

from langchain_leap0 import Leap0Sandbox

client = Leap0Client()
sandbox = client.sandboxes.create()
backend = Leap0Sandbox(client=client, sandbox=sandbox)

try:
    result = backend.execute("echo 'Hello LangChain from Leap0.dev'")
    print(result.output)
finally:
    client.sandboxes.delete(sandbox)
    client.close()
```

## Examples

Runnable scripts for [Deep Agents sandboxes](https://docs.langchain.com/oss/python/deepagents/sandboxes). See `[examples/README.md](examples/README.md)` for environment variables and how they map to LangChain `**SandboxIntegrationTests**`.


| Script                                                                 | Summary                                                                                                            |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `[examples/basic_sandbox.py](examples/basic_sandbox.py)`               | Minimal: create a sandbox, `Leap0Sandbox.execute()`, teardown.                                                     |
| `[examples/sandbox_backend_ops.py](examples/sandbox_backend_ops.py)`   | `execute`, `write`/`read`/`edit`, `upload_files`/`download_files`, `invalid_path` on relative download.            |
| `[examples/deep_agent_sandbox.py](examples/deep_agent_sandbox.py)`     | `create_deep_agent(..., backend=Leap0Sandbox(...))` — create and run a script; prints a short **execute** summary. |
| `[examples/deep_agent_workspace.py](examples/deep_agent_workspace.py)` | Multi-step file + shell task (POSIX `notes.txt` + `wc -l`); execute summary and final model reply.                 |


From the repo root:

```bash
uv run python examples/basic_sandbox.py
uv run python examples/sandbox_backend_ops.py
uv run python examples/deep_agent_sandbox.py
uv run python examples/deep_agent_workspace.py
```

## Developing from source

From this directory (alongside `leap0-python` in the Leap0 workspace). Uses `pyproject.toml` dependencies; run:

```bash
cd langchain-leap0
uv sync --all-groups
```

`[project.urls]` in `pyproject.toml` points at [github.com/leap0-dev/langchain-leap0](https://github.com/leap0-dev/langchain-leap0). The Python SDK lives under the same org: `[leap0-dev/leap0-python](https://github.com/leap0-dev/leap0-python)`.

## Documentation

Full documentation is available at [leap0.dev/docs](https://leap0.dev/docs).

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.