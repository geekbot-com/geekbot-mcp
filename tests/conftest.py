import os
from pathlib import Path

import pytest


@pytest.fixture
def api_key():
    """Get API key from environment variables."""
    key = os.environ.get("GB_API_KEY")
    if not key:
        pytest.skip("GB_API_KEY environment variable not set")
    return key


@pytest.fixture
def env_with_api_key():
    """Create environment variables dictionary with API key for subprocess"""
    env = os.environ.copy()
    api_key = os.environ.get("GB_API_KEY")
    if not api_key:
        pytest.skip("GB_API_KEY environment variable not set")
    env["GB_API_KEY"] = api_key
    return env


@pytest.fixture
def server_path():
    """Return the path to the main server file"""
    return Path(__file__).parent.parent / "geekbot_mcp" / "server.py"
