import urllib3
import multiprocessing
from nginxPlusAPI import KeyValueStore
from nginxPlusAPI import Upstreams

class Client(object):

  def __init__(self, host, poolSize=multiprocessing.cpu_count()):
    super().__init__()
    self.host = host
    self._poolSize = poolSize
    self._HTTPPool = urllib3.connectionpool.connection_from_url(host, maxsize=poolSize)
    self.HTTPUpstreams = Upstreams(self, 'http')
    self.StreamUpstreams = Upstreams(self, 'stream')
    self._KeyValueStoreFactory = KeyValueStore

  def KeyValueStore(self, zone, values=None):
    return self._KeyValueStoreFactory(self, zone, values)
  
  def request(self, *args, **kwargs):
    return self._HTTPPool.request(*args, **kwargs)