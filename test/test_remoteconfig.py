import time

import httpretty

from remoteconfig import config, RemoteConfig


class TestRemoteConfig(object):
  @httpretty.activate
  def test_read(self):
    config_url = 'http://test-remoteconfig.com/config.ini'

    config_content = '[section]\n\nkey = value\n'
    httpretty.register_uri(httpretty.GET, config_url, body=config_content)
    config.read(config_url)
    assert config_content == str(config)

    # Using cache duration
    updated_config_content = '[section]\n\nkey = updated\n'
    httpretty.register_uri(httpretty.GET, config_url, body=updated_config_content)
    config2 = RemoteConfig(config_url, cache_duration=1, kv_sep=': ')
    assert config_content.replace(' = ', ': ') == str(config2)

    # Still under cache duration
    config2.read(config_url)
    assert config_content.replace(' = ', ': ') == str(config2)

    time.sleep(1)
    # Should update after cache duration
    config.read(config_url)
    assert updated_config_content == str(config)
