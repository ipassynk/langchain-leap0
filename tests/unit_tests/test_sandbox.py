from __future__ import annotations

from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import cast
from unittest.mock import MagicMock

import pytest
from leap0 import Leap0Error, Sandbox as Leap0SdkSandbox
from leap0.models.sandbox import Sandbox

from langchain_leap0 import Leap0Sandbox
from langchain_leap0.sandbox import Leap0Sandbox as Leap0SandboxCls


@dataclass(slots=True)
class _ConnectedSandboxStub(Sandbox):
    """Minimal ``SandboxHandle`` with mocked services (matches connected SDK shape)."""

    process: object | None = field(default=None)
    filesystem: object | None = field(default=None)


def _make_backend(
    *, sandbox: _ConnectedSandboxStub | None = None
) -> tuple[Leap0Sandbox, MagicMock]:
    client = MagicMock()
    if sandbox is None:
        sandbox = _ConnectedSandboxStub(
            id="sb-123",
            process=client.process,
            filesystem=client.filesystem,
        )
    backend = Leap0Sandbox(
        client=client,
        sandbox=cast(Leap0SdkSandbox, sandbox),
    )
    return backend, client


def test_id_from_connected_handle() -> None:
    backend, _ = _make_backend(
        sandbox=_ConnectedSandboxStub(
            id="my-sandbox-id",
            process=MagicMock(),
            filesystem=MagicMock(),
        ),
    )
    assert backend.id == "my-sandbox-id"


def test_execute_returns_response() -> None:
    backend, client = _make_backend()
    client.process.execute.return_value = SimpleNamespace(
        stdout="hello\n",
        stderr="",
        exit_code=0,
    )
    result = backend.execute("echo hello")
    assert result.output == "hello\n"
    assert result.exit_code == 0
    assert result.truncated is False
    client.process.execute.assert_called_once()
    kwargs = client.process.execute.call_args.kwargs
    assert kwargs["command"] == "echo hello"
    assert kwargs["timeout"] == 30 * 60


def test_execute_respects_explicit_timeout() -> None:
    backend, client = _make_backend()
    client.process.execute.return_value = SimpleNamespace(
        stdout="",
        stderr="",
        exit_code=0,
    )
    backend.execute("true", timeout=42)
    assert client.process.execute.call_args.kwargs["timeout"] == 42


def test_download_invalid_path_skips_api() -> None:
    backend, client = _make_backend()
    responses = backend.download_files(["relative/path.txt"])
    assert len(responses) == 1
    assert responses[0].path == "relative/path.txt"
    assert responses[0].error == "invalid_path"
    assert responses[0].content is None
    client.filesystem.read_bytes.assert_not_called()


@pytest.mark.parametrize(
    ("status", "body", "expected"),
    [
        (404, "", "file_not_found"),
        (403, "", "permission_denied"),
        (500, "is a directory", "is_directory"),
        (500, "other", "permission_denied"),
    ],
)
def test_download_maps_api_errors(
    status: int,
    body: str,
    expected: str,
) -> None:
    backend, client = _make_backend()
    client.filesystem.read_bytes.side_effect = Leap0Error(
        "request failed",
        status,
        body=body,
    )
    responses = backend.download_files(["/file.txt"])
    assert responses[0].error == expected
    assert responses[0].content is None


def test_download_success() -> None:
    backend, client = _make_backend()
    client.filesystem.read_bytes.return_value = b"payload"
    responses = backend.download_files(["/a"])
    assert responses[0].content == b"payload"
    assert responses[0].error is None


def test_upload_invalid_path_skips_api() -> None:
    backend, client = _make_backend()
    responses = backend.upload_files([("relative", b"x")])
    assert responses[0].error == "invalid_path"
    client.filesystem.write_bytes.assert_not_called()


def test_upload_success() -> None:
    backend, client = _make_backend()
    responses = backend.upload_files([("/tmp/f", b"data")])
    assert responses[0].error is None
    client.filesystem.write_bytes.assert_called_once()


def test_map_filesystem_api_error_directory_message() -> None:
    exc = Leap0Error("read failed", 400, body="path is a directory")
    assert Leap0SandboxCls._map_filesystem_api_error(exc) == "is_directory"
