import os
from datetime import datetime, timedelta

import pytest

from geekbot_mcp.geekbot_api import GeekbotAPI


@pytest.fixture
def api_key():
    """Fixture to provide API key from environment variables."""
    key = os.environ.get("GB_API_KEY")
    if not key:
        pytest.skip("GB_API_KEY environment variable not set")
    return key


@pytest.fixture
def gb_api_client(api_key):
    """Fixture to provide a GeekbotAPI instance."""
    return GeekbotAPI(api_key=api_key)


@pytest.mark.asyncio
async def test_get_standups(gb_api_client):
    """Test fetching standups list."""
    async with gb_api_client as api:
        standups = await api.get_standups()
        assert isinstance(standups, list)
        if len(standups) > 0:
            # Verify standup structure if any exist
            standup = standups[0]
            assert "id" in standup
            assert "name" in standup


@pytest.mark.asyncio
async def test_get_reports(gb_api_client):
    """Test fetching reports."""
    async with gb_api_client as api:
        reports = await api.get_reports()
        assert isinstance(reports, list)
        if len(reports) > 0:
            # Verify report structure if any exist
            report = reports[0]
            assert "id" in report
            assert "standup_id" in report


@pytest.mark.asyncio
async def test_get_reports_with_filters(gb_api_client):
    """Test fetching reports with various filters."""
    # Test with standup_id filter
    async with gb_api_client as api:
        today = datetime.now()
        week_ago = today - timedelta(days=7)

        reports = await api.get_reports(
            after=week_ago.timestamp(), before=today.timestamp()
        )
        assert isinstance(reports, list)
        assert len(reports) > 0
