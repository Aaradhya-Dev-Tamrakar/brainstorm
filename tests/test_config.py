from pilot.config import PilotConfig

def test_pilot_config_auth():
    config = PilotConfig(token="ghp_test123", orgs=["Aaradhya-Dev-Tamrakar"], users=["AaradhyaDT"])
    assert config.has_auth is True
    headers = config.get_auth_headers()
    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer ghp_test123"
    assert "Aaradhya-Dev-Tamrakar" in config.orgs
    assert "AaradhyaDT" in config.users

def test_pilot_config_unauthenticated():
    config = PilotConfig(token=None)
    assert config.has_auth is False
    headers = config.get_auth_headers()
    assert "Authorization" not in headers

def test_pilot_config_defaults():
    config = PilotConfig()
    assert len(config.orgs) >= 1
    assert config.cache_ttl_seconds > 0
