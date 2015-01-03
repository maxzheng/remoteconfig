from localconfig.manager import DotNotationConfig
import requests

from remoteconfig.utils import url_content


class RemoteConfig(DotNotationConfig):
  def read(self, source, cache_duration=None):
    """
      Reads and parses the config source

      :param file/str source: Config source URL (http/https), or string, file name, or file pointer.
      :param int cache_duration: For URL source only. Optionally cache the URL content for the given duration (seconds) to
                                 avoid downloading too often.
    """
    if source.startswith('http://') or source.startswith('https://'):
      source = url_content(source, cache_duration, from_cache_on_error=True)

    return super(RemoteConfig, self).read(source)
