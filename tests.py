import unittest
from kitten import KittenFS
from util import hashed_key, get_meta_data
kitten = KittenFS()
kitten.create_master()
kitten.add_worker()
class TestKittenFS(unittest.TestCase):
     
    # these need to be run before
    def test_a_put(self):
        result = kitten.put('A', 'hello')
        self.assertEqual(result, 'hello')
    def test_b_put(self):
        result = kitten.put('B', 'bye')
        self.assertEqual(result, 'bye')
    def test_c_get(self): 
        kitten.put('A', 'hello')
        result = kitten.get('A')
        self.assertEqual(result, 'hello'.encode())
    def test_d_delete(self):
        kitten.put('B', 'bye')
        result = kitten.delete('B', with_hash=False, is_testing=True)
        self.assertEqual(result, hashed_key('B').encode())
    def test_e_add_worker_to_master(self):
        meta_data = get_meta_data(kitten.worker_idx)
        h_key = hashed_key(kitten.worker_idx)
        result = kitten.add_worker_to_master(str(h_key).encode(), str(meta_data).encode())
        self.assertEqual(str(h_key).encode(), result)
    def test_f_clear_worker(self):
        result = kitten.clear_worker(testing=True)
        self.assertEqual(result, "Cleared worker")
    def test_g_clear_master(self):
        result = kitten.clear_master()
        self.assertEqual(result, "Cleared master")
    def test_h_close_worker(self):
        result = kitten.close_worker()
        self.assertEqual(result, "closed worker " + str(kitten.worker_idx))
    def test_i_close_master(self):
        result = kitten.close_master()
        self.assertEqual(result, "closed master")


if __name__ == "__main__":
    unittest.main()
