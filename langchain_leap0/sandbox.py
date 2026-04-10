"""Leap0 sandbox backend implementation."""

from __future__ import annotations

from http import HTTPStatus
from typing import Any

from deepagents.backends.protocol import (
    ExecuteResponse,
    FileDownloadResponse,
    FileOperationError,
    FileUploadResponse,
)
from deepagents.backends.sandbox import BaseSandbox
from leap0 import Leap0Client, Leap0Error, Sandbox


class Leap0Sandbox(BaseSandbox):
    """Leap0 sandbox implementation conforming to SandboxBackendProtocol."""

    def __init__(
        self,
        *,
        client: Leap0Client,
        sandbox: Sandbox,
        timeout: int = 30 * 60,
    ) -> None:
        """Create a backend connected to an existing Leap0 sandbox.

        Args:
            client: Authenticated Leap0 API client.
            sandbox: Connected handle from the SDK (e.g. ``leap0.Sandbox`` from
                ``client.sandboxes.create()`` or ``get()``).
            timeout: Default command timeout in seconds when ``execute()`` is
                called without an explicit ``timeout``.
        """
        self._client = client
        self._sandbox = sandbox
        self._sandbox_id = sandbox.id
        self._process: Any = sandbox.process
        self._filesystem: Any = sandbox.filesystem
        self._default_timeout = timeout

    @property
    def id(self) -> str:
        """Return the Leap0 sandbox id."""
        return self._sandbox_id

    def execute(self, command: str, *, timeout: int | None = None) -> ExecuteResponse:
        """Execute a shell command inside the sandbox.

        Args:
            command: Shell command string to execute.
            timeout: Maximum time in seconds to wait for this command.

                If None, uses the backend's default timeout.

        Returns:
            ExecuteResponse containing output, exit code, and truncation flag.
        """
        effective_timeout = timeout if timeout is not None else self._default_timeout
        result = self._process.execute(
            command=command,
            timeout=effective_timeout,
        )
        output = result.stdout
        if result.stderr:
            output += result.stderr if not output else f"\n{result.stderr}"
        return ExecuteResponse(
            output=output,
            exit_code=result.exit_code,
            truncated=False,
        )

    def download_files(self, paths: list[str]) -> list[FileDownloadResponse]:
        """Download files from the sandbox.

        Non-absolute paths return ``invalid_path`` without calling the API.
        Failures are reported per path via ``FileDownloadResponse.error``.
        """
        responses: list[FileDownloadResponse] = []
        for path in paths:
            if not path.startswith("/"):
                responses.append(
                    FileDownloadResponse(path=path, content=None, error="invalid_path"),
                )
                continue
            try:
                content = self._filesystem.read_bytes(path=path)
            except Leap0Error as exc:
                responses.append(
                    FileDownloadResponse(
                        path=path,
                        content=None,
                        error=self._map_filesystem_api_error(exc),
                    ),
                )
            except Exception as exc:  # noqa: BLE001
                responses.append(
                    FileDownloadResponse(
                        path=path,
                        content=None,
                        error=self._map_generic_filesystem_error(exc),
                    ),
                )
            else:
                responses.append(
                    FileDownloadResponse(path=path, content=content, error=None),
                )
        return responses

    def upload_files(self, files: list[tuple[str, bytes]]) -> list[FileUploadResponse]:
        """Upload files into the sandbox.

        Non-absolute paths return ``invalid_path`` without calling the API.
        Failures are reported per file via ``FileUploadResponse.error``.
        """
        responses: list[FileUploadResponse] = []
        for path, content in files:
            if not path.startswith("/"):
                responses.append(FileUploadResponse(path=path, error="invalid_path"))
                continue
            try:
                self._filesystem.write_bytes(path=path, content=content)
            except Leap0Error as exc:
                responses.append(
                    FileUploadResponse(
                        path=path,
                        error=self._map_filesystem_api_error(exc),
                    ),
                )
            except Exception as exc:  # noqa: BLE001
                responses.append(
                    FileUploadResponse(
                        path=path,
                        error=self._map_generic_filesystem_error(exc),
                    ),
                )
            else:
                responses.append(FileUploadResponse(path=path, error=None))
        return responses

    @staticmethod
    def _map_filesystem_api_error(exc: Leap0Error) -> FileOperationError:
        """Map Leap0 HTTP errors to ``FileOperationError`` literals."""
        combined = f"{exc.message} {exc.body or ''}".lower()
        if exc.status_code == HTTPStatus.NOT_FOUND:
            return "file_not_found"
        if exc.status_code == HTTPStatus.FORBIDDEN:
            return "permission_denied"
        if "not a regular file" in combined or "is a directory" in combined:
            return "is_directory"
        return "permission_denied"

    @staticmethod
    def _map_generic_filesystem_error(_exc: Exception) -> FileOperationError:
        """Map non-HTTP filesystem failures to a stable file operation error."""
        return "permission_denied"
