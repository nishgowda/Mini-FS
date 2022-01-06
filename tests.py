import unittest
from diststore import DistStore

dstore = DistStore()
class TestDistStore(unittest.TestCase):
    
    def test_create_master(self):
        master = dstore.create_master()
        self.assertRegex(str(master), "<plyvel.DB with name '/tmp/cachedb/master'")
    def test_add_worker(self):
        worker = dstore.add_worker()
        self.assertRegex(str(worker), "<plyvel.DB with name '/tmp/cachedb/worker/0'")
    def test_put(self):
        result = dstore.put(0, 'A')
        self.assertEqual(result, 'A')
    def test_get(self): 
        result = dstore.get(0)
        self.assertEqual(result, 'A'.encode())

if __name__ == "__main__":
    unittest.main()
