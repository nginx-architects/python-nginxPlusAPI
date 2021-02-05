import json

class KeyValueStore(dict):
  def __init__(self, client, zone, values=None):
    self._zone = zone
    self._client = client
    self._initValues = values
    self._cache = {}
    if isinstance(values,dict):
      for key in values:
        self.set(key, values[key])
    elif values is not None:
      raise TypeError("Incompatible type for values. Must be dict or None. Class type "+ str(values.__class__) + " used")

  def set(self, key, value):
    method = 'POST'
    v = self.get(key)
    if v == value:
      print('New value and old value are the same')
      return
    if v:
      method = 'PATCH'
    body = {
      key: value
    }
    r = self._client.request(method, "/api/6/http/keyvals/" + self._zone, body=json.dumps(body))
    if r.status != 201 and r.status != 204:
      raise KeyError("Could not store key value. " + str(r.status) + ": " + r.reason)

  def get(self, key):
    r = self._client.request('GET',"/api/6/http/keyvals/" + self._zone)
    self._cache = json.loads(r.data)
    if r.status != 200 and r.status != 404:
      raise str(r.status) + ": " + r.reason
    if key in self._cache:
      return self._cache[key]
    return None

  def getAll(self):
    r = self._client.request('GET',"/api/6/http/keyvals/" + self._zone)
    self._cache = json.loads(r.data)
    if r.status != 200 and r.status != 404:
      raise str(r.status) + ": " + r.reason
    return self._cache

  def deleteAll(self):
    r = self._client.request('delete',"/api/6/http/keyvals/" + self._zone)
    if r.status != 204:
      raise BaseException(str(r.status) + ": " + r.reason)
    return

  def items(self):
    return self.getAll().keys()
  
  def keys(self):
    return self.getAll().keys()

  def __setitem__(self, key, value):
    if isinstance(key, str):
      self.set(key,value)
    return
    
  def __getitem__(self, key):
    if isinstance(key, str):
      return self.get(key)
    
  def __iter__(self):
    return self.getAll().__iter__()

  def __repr__(self):
    return self.getAll().__repr__()
  
  def __str__(self):
    return self.getAll().__str__()

  def __len__(self):
    return self.getAll().__len__()

  def __delitem__(self, key):
    if isinstance(key, str):
      return self.set(key,None)
    raise TypeError("key object must be string")

  def __contains__(self, key):
    if isinstance(key, str):
      return key in self.getAll()
    raise TypeError("key object must be string")

  def __del__(self):
    self.deleteAll()
    return