import unittest
from types import SimpleNamespace
from nginxPlusAPI import Client
from pprint import pprint as pp

class TestHTTPUpstreams(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestHTTPUpstreams,self).__init__(*args, **kwargs)
    self.client = Client("http://localhost:8000")
  
  def test_getHTTPAllUpstreams(self):
    assert len(self.client.HTTPUpstreams.getAllUpstreams().test2.peers) == 5
    return True

  def test_getHTTPUpstream(self):
    assert len(self.client.HTTPUpstreams.getUpstream('test2').peers) == 5
    return True

  def test_getHTTPUpstreamServer(self):
    assert isinstance(self.client.HTTPUpstreams.getUpstreamServer('test2', 0), SimpleNamespace)
    return True

  def test_getHTTPUpstreamServers(self):
    assert len(self.client.HTTPUpstreams.getUpstreamServers('test2')) == 5
    return True

  def test_addAndDeleteHTTPServer(self):
    originalPeerCount = len(self.client.HTTPUpstreams.getUpstream('test').peers)
    addedServer = self.client.HTTPUpstreams.addServer('test','192.168.1.1')
    assert self.client.HTTPUpstreams.getUpstreamServer('test', addedServer.id).server == '192.168.1.1:80'
    assert len(self.client.HTTPUpstreams.deleteServer('test', addedServer.id)) == originalPeerCount
    return True

  def test_addHTTPServerByDict(self):
    server = {
      'server': '192.168.1.21'
    }
    addedServer = self.client.HTTPUpstreams.addServerByDict('test', server)
    assert self.client.HTTPUpstreams.getUpstreamServer('test', addedServer.id).server == '192.168.1.21:80'
    self.client.HTTPUpstreams.deleteServer('test', addedServer.id)
    return True

  def test_resetHTTPStats(self):
    return self.client.HTTPUpstreams.resetStats('test2')

  def test_setHTTPServerDownUP(self):
    assert self.client.HTTPUpstreams.setServerDown('test2',1).down == True
    assert self.client.HTTPUpstreams.setServerUp('test2',1).down == False
    return True

  def test_setHTTPServerDrain(self):
    assert self.client.HTTPUpstreams.setServerDrain('test2',2).drain == True
    assert self.client.HTTPUpstreams.setServerUp('test2',1).down == False
    return True

  def test_setHTTPServerFlag(self):
    assert self.client.HTTPUpstreams.setServerFlag('test2',1,'down','true').down == True
    assert self.client.HTTPUpstreams.setServerFlag('test2',1,'down', 'false').down == False
    return True

  def test_setHTTPServerFlagByDict(self):
    flag = {
      'id': '1',
      'down': 'true'
    }
    assert self.client.HTTPUpstreams.setServerFlagByDict('test2',flag).down == True
    assert self.client.HTTPUpstreams.setServerUp('test2',1).down == False
    return True

    
class TestStreamUpstreams(unittest.TestCase):

  def __init__(self, *args, **kwargs):
    super(TestStreamUpstreams,self).__init__(*args, **kwargs)
    self.client = Client("http://localhost:8000")
  
  def test_getStreamAllUpstreams(self):
    assert len(self.client.StreamUpstreams.getAllUpstreams().test2.peers) == 5
    return True

  def test_getStreamUpstream(self):
    assert len(self.client.StreamUpstreams.getUpstream('test2').peers) == 5
    return True

  def test_getStreamUpstreamServer(self):
    assert isinstance(self.client.StreamUpstreams.getUpstreamServer('test2', 0), SimpleNamespace)
    return True

  def test_getStreamUpstreamServers(self):
    assert len(self.client.StreamUpstreams.getUpstreamServers('test2')) == 5
    return True

  def test_addAndDeleteStreamServer(self):
    originalPeerCount = len(self.client.StreamUpstreams.getUpstream('test').peers)
    addedServer = self.client.StreamUpstreams.addServer('test','192.168.1.1:80')
    assert self.client.StreamUpstreams.getUpstreamServer('test', addedServer.id).server == '192.168.1.1:80'
    assert len(self.client.StreamUpstreams.deleteServer('test', addedServer.id)) == originalPeerCount
    return True

  def test_addStreamServerByDict(self):
    server = {
      'server': '192.168.1.21:80'
    }
    addedServer = self.client.StreamUpstreams.addServerByDict('test', server)
    assert self.client.StreamUpstreams.getUpstreamServer('test', addedServer.id).server == '192.168.1.21:80'
    self.client.StreamUpstreams.deleteServer('test', addedServer.id)
    return True

  def test_resetStreamStats(self):
    self.client.StreamUpstreams.resetStats('test')
    return True

  def test_setStreamServerDownUP(self):
    assert self.client.StreamUpstreams.setServerDown('test2',1).down == True
    assert self.client.StreamUpstreams.setServerUp('test2',1).down == False
    return True

  def test_setStreamServerDrain(self):
    try:
      self.client.StreamUpstreams.setServerDrain('test2',2).drain == True
    except BaseException as e:
      assert isinstance(e, BaseException)
    return True

  def test_setStreamServerFlag(self):
    assert self.client.StreamUpstreams.setServerFlag('test2',1,'down','true').down == True
    assert self.client.StreamUpstreams.setServerFlag('test2',1,'down', 'false').down == False
    return True

  def test_setStreamServerFlagByDict(self):
    flag = {
      'id': '1',
      'down': 'true'
    }
    assert self.client.StreamUpstreams.setServerFlagByDict('test2',flag).down == True
    assert self.client.StreamUpstreams.setServerUp('test2',1).down == False
    return True