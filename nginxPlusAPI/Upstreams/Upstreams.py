import json
from types import SimpleNamespace

class Upstreams(object):
  def __init__(self, client, type):
    self._type = type
    self._client = client

  def getUpstream(self, upstream):
    r = self._client.request('GET',"/api/6/" + self._type + "/upstreams/" + upstream)
    upstreamInfo = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 200 and r.status != 404:
      raise str(r.status) + ": " + r.reason
    if isinstance(upstreamInfo, SimpleNamespace):
      return upstreamInfo
    return None

  def getUpstreamServer(self, upstream, server):
    r = self._client.request('GET',"/api/6/" + self._type + "/upstreams/" + upstream + "/servers/" + str(server))
    serverInfo = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 200 and r.status != 404:
      raise str(r.status) + ": " + r.reason
    if isinstance(serverInfo, SimpleNamespace):
      return serverInfo
    return None

  def getUpstreamServers(self, upstream):
    r = self._client.request('GET',"/api/6/" + self._type + "/upstreams/" + upstream + "/servers")
    upstreamInfo = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 200 and r.status != 404:
      raise str(r.status) + ": " + r.reason
    if isinstance(upstreamInfo, list):
      return upstreamInfo
    return None

  def getAllUpstreams(self):
    r = self._client.request('GET',"/api/6/" + self._type + "/upstreams")
    upstreams = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 200 and r.status != 404:
      raise str(r.status) + ": " + r.reason
    if isinstance(upstreams, SimpleNamespace):
      return upstreams
    return None

  def addServer(self, upstream, server, **kwargs):
    kwargs['server'] = server
    return self.addServerByDict(upstream, kwargs)

  def addServerByDict(self, upstream, server):
    headers = {
      "Content-Type": "application/json"
    }
    if not isinstance(server, dict):
      raise TypeError('server must be a dict')
    r = self._client.request(
      'POST',"/api/6/" + self._type + "/upstreams/" + upstream + "/servers/",
      body = json.dumps(server),
      headers = headers
    )
    serverInfo = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 201:
      raise BaseException(str(r.status) + ": " + r.reason + "->" + json.dumps(json.loads(r.data)))
    if isinstance(serverInfo, SimpleNamespace):
      return serverInfo
    return None

  def deleteServer(self, upstream, server):
    r = self._client.request('DELETE',"/api/6/" + self._type + "/upstreams/" + upstream + "/servers/" + str(server))
    serverInfo = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 200:
      raise BaseException(str(r.status) + ": " + r.reason + "->" + json.dumps(json.loads(r.data)))
    return serverInfo

  def resetStats(self, upstream):
    r = self._client.request('DELETE',"/api/6/" + self._type + "/upstreams/" + upstream)
    if r.status != 204:
      raise BaseException(str(r.status) + ": " + r.reason)
    return True

  def setServerDown(self, upstream, server):
    return self.setServerFlag(upstream, server, 'down', 'true')
  
  def setServerUp(self, upstream, server):
    return self.setServerFlag(upstream, server, 'down', 'false')

  def setServerDrain(self, upstream, server):
    return self.setServerFlag(upstream, server, 'drain', 'true')

  def setServerFlag(self, upstream, server, stateFlag, state):
    serverState = {
      'id': str(server),
      stateFlag: state
    }

    return self.setServerFlagByDict(upstream, serverState)

  def setServerFlagByDict(self, upstream, server):
    headers = {
      "Content-Type": "application/json"
    }
    serverID = server['id']
    del server['id']
    if not isinstance(server, dict):
      raise TypeError('server must be a dict')
    r = self._client.request(
      'PATCH',"/api/6/" + self._type + "/upstreams/" + upstream + "/servers/" + serverID,
      body = json.dumps(server),
      headers = headers
    )
    serverInfo = json.loads(r.data, object_hook=lambda d: SimpleNamespace(**d))
    if r.status != 200:
      raise BaseException(str(r.status) + ": " + r.reason + "->" + json.dumps(json.loads(r.data)))
    if isinstance(serverInfo, SimpleNamespace):
      return serverInfo
    return None