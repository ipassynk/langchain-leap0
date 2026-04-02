#!/usr/bin/env bash
set -euo pipefail

uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_no_overrides_DO_NOT_OVERRIDE" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_write_new_file" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_read_basic_file" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_edit_single_occurrence" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_ls_info_lists_files" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_glob_info" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_grep_raw_literal" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_upload_single_file" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_download_single_file" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_upload_download_roundtrip" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_upload_multiple_files_order_preserved" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_download_multiple_files_order_preserved" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_upload_binary_content_roundtrip" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_download_error_file_not_found" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_download_error_is_directory" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_download_error_permission_denied" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_download_error_invalid_path_relative" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_upload_missing_parent_dir_or_roundtrip" -vv -s
uv run --group test pytest "tests/integration_tests/test_integration.py::TestLeap0SandboxStandard::test_upload_relative_path_returns_invalid_path" -vv -s
