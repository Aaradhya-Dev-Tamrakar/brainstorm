import pytest
from pilot.mcp_server import mcp

def test_mcp_server_tools():
    # Verify all 4 tools are registered
    tool_names = [t.name for t in mcp._tool_manager.list_tools()]
    assert "get_fleet_health" in tool_names
    assert "scrape_trending" in tool_names
    assert "get_changelog_digest" in tool_names
    assert "generate_profile_assets" in tool_names
