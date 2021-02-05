from logging import exception
import unittest
import yaml
import requests
import json
from nginxPlusAPI import Client
from pprint import pprint as pp

configFile = "./configs/testConfig.yaml"

class TestKeyValueStore(unittest.TestCase):

   @classmethod
   def setUp(kclass):
      f = open(configFile,'r')
      config = yaml.safe_load(f)
      f.close()
      r = requests.delete(config['host']+"/api/6/http/keyvals/test_zone")
      assert r.status_code == 204
      pp(r)

   def __init__(self, *args, **kwargs):
      super(TestKeyValueStore,self).__init__(*args, **kwargs)
      f = open(configFile,'r')
      self.config = yaml.safe_load(f)
      f.close()
      self.client = Client(self.config['host'])
         

   def test_creatingObject(self):
      k = self.client.KeyValueStore('test_zone')
      assert k is not None
      assert k._client is not None
      return True

   def test_creatingObjectWithValue(self):
      value = {
         "foo": "bar"
      }
      k = self.client.KeyValueStore('test_zone', value)
      assert k is not None
      assert k._client is not None
      r = requests.get(self.config['host']+"/api/6/http/keyvals/test_zone")
      assert r is not None
      keyValue = json.loads(r.content)
      pp(keyValue)
      assert keyValue['foo'] == 'bar'
      return True

   def test_creatingObjectWithBadValue(self):
      try:
         k = self.client.KeyValueStore('test_zone', "foobar")
      except Exception as e:
         assert isinstance(e,TypeError)
         print(e.__str__())
         assert "Incompatible type for values. Must be dict or None. Class type" in e.__str__()
      
      return True

   def test_set(self):
      k = self.client.KeyValueStore('test_zone')
      assert k is not None
      k.set('foo','bar')
      r = requests.get(self.config['host']+"/api/6/http/keyvals/test_zone")
      assert r is not None
      keyValue = json.loads(r.content)
      assert keyValue['foo'] == 'bar'
      return True

   def test_set_same(self):
      k = self.client.KeyValueStore('test_zone')
      assert k is not None
      k.set('foo','bar')
      k.set('foo','bar')
      r = requests.get(self.config['host']+"/api/6/http/keyvals/test_zone")
      assert r is not None
      keyValue = json.loads(r.content)
      assert keyValue['foo'] == 'bar'
      return True

   def test_set_None(self):
      k = self.client.KeyValueStore('test_zone')
      assert k is not None
      k.set('foo',None)
      r = requests.get(self.config['host']+"/api/6/http/keyvals/test_zone")
      assert r is not None
      keyValue = json.loads(r.content)
      assert 'foo' not in keyValue
      return True

   def test_get(self):
      k = self.client.KeyValueStore('test_zone')
      assert k is not None
      k.set('foo','bar')
      r = k.get('foo')
      assert r == 'bar'
      return True
   
   def test_get_None(self):
      k = self.client.KeyValueStore('test_zone')
      assert k is not None
      r = k.get('foo')
      assert r == None
      return True

   def test_dict(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      pp(k)
      assert k['foo'] == 'bar'
      return True
   
   def test_dict_iter(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      k['monekey'] = 'butt'
      k['NGINX'] = 'ROXS'
      for key in k:
         print(key+": "+k[key])
      return True

   def test_items(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      k['monkey'] = 'butt'
      k['NGINX'] = 'ROXS'
      items = k.items()
      assert 'foo' in items
      assert 'monkey' in items
      assert 'NGINX' in items
      pp(items)
      return
   
   def test_keys(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      k['monkey'] = 'butt'
      k['NGINX'] = 'ROXS'
      keys = k.keys()
      assert 'foo' in keys
      assert 'monkey' in keys
      assert 'NGINX' in keys
      pp(keys)
      return

   def test_contains(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      k['monkey'] = 'butt'
      k['NGINX'] = 'ROXS'
      assert  'foo' in k
      assert 'monkey' in k
      assert 'NGINX' in k
      pp(k)
      return

   def test_delete_item(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      k['monkey'] = 'butt'
      k['NGINX'] = 'ROXS'
      del k['monkey']
      keys = k.keys()
      assert  k['foo'] == 'bar'
      assert 'monkey' not in keys
      assert k['NGINX'] == 'ROXS'
      pp(k)
      return

   def test_delete(self):
      k = self.client.KeyValueStore('test_zone')
      k['foo'] = 'bar'
      k['monkey'] = 'butt'
      k['NGINX'] = 'ROXS'
      del k
      assert 'k' not in locals()
      return

