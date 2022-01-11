import unittest
from kitten import KittenFS
from util import hashed_key
kitten = KittenFS()
kitten.create_master()
kitten.add_worker()
class TestKittenFS(unittest.TestCase):
     
    # these need to be run before
    def test_put(self):
        result = kitten.put('A', 'hello')
        self.assertEqual(result, 'hello')
    def test_put_B(self):
        result = kitten.put('B', 'bye')
        self.assertEqual(result, 'bye')
    def test_get(self): 
        kitten.put('A', 'hello')
        result = kitten.get('A')
        self.assertEqual(result, 'hello'.encode())
    def test_delete(self):
        kitten.put('B', 'bye')
        result = kitten.delete('B')
        self.assertEqual(result, hashed_key('B').encode())
if __name__ == "__main__":
    unittest.main()
