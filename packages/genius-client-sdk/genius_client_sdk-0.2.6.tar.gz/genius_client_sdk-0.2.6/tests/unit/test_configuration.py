import os

from genius_client_sdk.configuration import default_agent_config, BaseAgentConfig


def test_defaults():
    assert BaseAgentConfig.DEFAULT_AGENT_PORT == 3000
    assert BaseAgentConfig.DEFAULT_AGENT_HOSTNAME == "localhost"
    assert BaseAgentConfig.DEFAULT_AGENT_HTTP_PROTOCOL == "http"


def test_live_configuration():
    assert default_agent_config.agent_port == 3000
    assert default_agent_config.agent_hostname == "localhost"
    assert default_agent_config.agent_http_protocol == "http"
    assert default_agent_config.agent_url == "http://localhost:3000"
    assert default_agent_config.build_version == "0.3.0"


def test_envvar_configuration():
    # Set environment variables
    os.environ["AGENT_PORT"] = "2222"
    os.environ["AGENT_HOSTNAME"] = "remotehost"
    os.environ["AGENT_HTTP_PROTOCOL"] = "https"

    try:
        # get a new instance of config (sort of fakes a reload with new env vars)
        new_config = BaseAgentConfig()

        # verify
        assert new_config.agent_port == 2222
        assert new_config.agent_hostname == "remotehost"
        assert new_config.agent_http_protocol == "https"
        assert new_config.agent_url == "https://remotehost:2222"
        assert new_config.build_version == "0.3.0"
    finally:
        # clean up
        del os.environ["AGENT_PORT"]
        del os.environ["AGENT_HOSTNAME"]
        del os.environ["AGENT_HTTP_PROTOCOL"]
