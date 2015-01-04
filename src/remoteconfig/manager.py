from localconfig.manager import DotNotationConfig
import requests

from remoteconfig.utils import url_content


class RemoteConfig(DotNotationConfig):
  def __init__(self, last_source=None, default_cache_duration=None, **localconfig_kwargs):
    """
    :param file/str last_source: Last config source, file or URL. This source is only read when an attempt to read a
                                 config value is made (delayed reading, hence "last") if it exists.
    :param int default_cache_duration: For URL source only. Optionally cache the URL content for the given duration (seconds) to
                               avoid downloading too often. This sets the default for all subsequent :meth:`self.read` calls.
    :param dict localconfig_kwargs: Additional keyword args to be passed to localconfig's :meth:`DotNotationConfig.__init__`
    """

    #: Default cache duration when reading from a URL source
    self._cache_duration = default_cache_duration

    super(RemoteConfig, self).__init__(last_source, **localconfig_kwargs)

  def read(self, source, cache_duration=None):
    """
    Reads and parses the config source

    :param file/str source: Config source URL (http/https), or string, file name, or file pointer.
    :param int cache_duration: For URL source only. Optionally cache the URL content for the given duration (seconds) to
                               avoid downloading too often. Overrides the default if that was set during instantiation.
    """
    if not cache_duration:
      cache_duration = self._cache_duration

    if source.startswith('http://') or source.startswith('https://'):
      source = url_content(source, cache_duration, from_cache_on_error=True)

    return super(RemoteConfig, self).read(source)
