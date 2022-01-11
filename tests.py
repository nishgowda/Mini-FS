import unittest
from kitten import KittenFS
from util import hashed_key
kitten = KittenFS()
class TestKittenFS(unittest.TestCase):
    
    def test_create_master(self):
        master = kitten.create_master()
        self.assertRegex(str(master), "<plyvel.DB with name '/tmp/cachedb/master'")
    def test_add_worker(self):
        worker = kitten.add_worker()
        self.assertRegex(str(worker), "<plyvel.DB with name '/tmp/cachedb/worker/0'")
    def test_put(self):
        result = kitten.put('A', 'hello')
        self.assertEqual(result, 'hello')
    def test_put_B(self):
        result = kitten.put('B', 'bye')
        self.assertEqual(result, 'bye')
    def test_get(self): 
        result = kitten.get('A')
        self.assertEqual(result, 'hello'.encode())
    def test_delete(self):
        result = kitten.delete('B')
        self.assertEqual(result, hashed_key('B').encode())
if __name__ == "__main__":
    unittest.main()
