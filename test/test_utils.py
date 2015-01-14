import os
import time

from mock import patch, Mock
import pytest

from remoteconfig.utils import url_content, _url_content_cache_file


def test_url_content():
  assert 'remoteconfig' in url_content('https://raw.githubusercontent.com/maxzheng/remoteconfig/master/docs/README.rst')

  with patch('requests.get') as requests_get:
    mock_response = Mock()
    mock_response.text = '[Messages]\n1: Test Message'
    requests_get.return_value = mock_response

    assert str(url_content('url1', cache_duration=1)) == mock_response.text

    cached_text = mock_response.text
    mock_response.text = '[Messages]\n1: Test Message Updated'

    # This should return cached content
    assert str(url_content('url1', cache_duration=1)) == cached_text
    requests_get.assert_called_once_with('url1', timeout=5)

    assert str(url_content('url2', cache_duration=1)) == mock_response.text

    time.sleep(1)

    assert str(url_content('url1', cache_duration=1)) == mock_response.text
    assert requests_get.call_count == 3

    # No content,it should raise
    cache_file = _url_content_cache_file('url3')
    if os.path.exists(cache_file):
      os.unlink(cache_file)

    requests_get.side_effect = Exception
    with pytest.raises(Exception):
      assert str(url_content('url3', from_cache_on_error=True)) == mock_response.text

    requests_get.side_effect = None
    assert str(url_content('url3', from_cache_on_error=True)) == mock_response.text

    requests_get.side_effect = Exception
    assert str(url_content('url3', from_cache_on_error=True)) == mock_response.text
