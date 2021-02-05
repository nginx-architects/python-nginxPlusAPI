import unittest
import yaml
import multiprocessing
from nginxPlusAPI import Client
from pprint import pprint as pp

configFile = "./configs/testConfig.yaml"

class TestClient(unittest.TestCase):

  def test_creatingObjectWithPoolSize(self):
      f = open(configFile,'r')
      config = yaml.safe_load(f)
      f.close()
      client = Client(config['host'], poolSize=int(config['poolSize']))
      assert client is not None
      print("poolSize: "+ str(client._poolSize) + " CPU Count: "+ str(multiprocessing.cpu_count()))
      assert client._poolSize == int(config['poolSize'])
      assert client.host == config['host']
      return True
   
  def test_creatingObjectWithoutPoolSize(self):
    f = open(configFile,'r')
    config = yaml.safe_load(f)
    f.close()
    client = Client(config['host'])
    assert client is not None
    print("poolSize: "+ str(client._poolSize) + " CPU Count: "+ str(multiprocessing.cpu_count()))
    assert client.host == config['host']
    assert client._poolSize == multiprocessing.cpu_count()
    return True