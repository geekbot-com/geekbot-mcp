import os

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
