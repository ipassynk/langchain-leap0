from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
from langchain_tests.integration_tests import SandboxIntegrationTests
from leap0 import Leap0Client

from langchain_leap0 import Leap0Sandbox

if TYPE_CHECKING:
    from collections.abc import Iterator

    from deepagents.backends.protocol import SandboxBackendProtocol


@pytest.mark.enable_socket()
class TestLeap0SandboxStandard(SandboxIntegrationTests):
    @pytest.fixture(scope="class")
    def sandbox(self) -> Iterator[SandboxBackendProtocol]:
        if not os.getenv("LEAP0_API_KEY"):
            pytest.skip("LEAP0_API_KEY is required for integration tests.")

        client = Leap0Client()
        sandbox = client.sandboxes.create()
        backend = Leap0Sandbox(client=client, sandbox=sandbox)
        try:
            yield backend
        finally:
            client.sandboxes.delete(sandbox)
            client.close()