import pytest

from geekbot_mcp.server import mcp


@pytest.mark.asyncio
async def test_mcp_tool_registration():
    """Test that the MCP server has the expected tools registered"""
    # Get the list of registered tools
    tools = await mcp.list_tools()
    tool_names = [tool.name for tool in tools]
    # Verify the expected tools are registered
    assert "fetch_standups" in tool_names
    assert "fetch_reports" in tool_names
