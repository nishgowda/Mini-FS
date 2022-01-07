import unittest
from diststore import DistStore
from util import hashed_key
dstore = DistStore()
class TestDistStore(unittest.TestCase):
    
    def test_create_master(self):
        master = dstore.create_master()
        self.assertRegex(str(master), "<plyvel.DB with name '/tmp/cachedb/master'")
    def test_add_worker(self):
        worker = dstore.add_worker()
        self.assertRegex(str(worker), "<plyvel.DB with name '/tmp/cachedb/worker/0'")
    def test_put(self):
        result = dstore.put('A', 'hello')
        self.assertEqual(result, 'hello')
    def test_put(self):
        result = dstore.put('B', 'bye')
        self.assertEqual(result, 'bye')
    def test_get(self): 
        result = dstore.get('A')
        self.assertEqual(result, 'hello'.encode())
    def test_delete(self):
        result = dstore.delete('B')
        self.assertEqual(result, hashed_key('B').encode())
if __name__ == "__main__":
    unittest.main()
