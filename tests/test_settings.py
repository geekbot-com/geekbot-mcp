import re

from geekbot_mcp.settings import load_package_info

# Define expected values for the test
EXPECTED_NAME = "geekbot-mcp"


def assert_expected_version_format(version: str):
    """Test that the expected version format is valid."""
    assert re.match(r"^\d+\.\d+\.\d+$", version)


def test_load_package_info():
    """Verify that load_package_info correctly reads name and version from the mock file."""
    name, version = load_package_info()
    assert name == EXPECTED_NAME
    assert_expected_version_format(version)
