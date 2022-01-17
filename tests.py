import unittest
from kitten import KittenFS
from util import hashed_key, get_meta_data
kitten = KittenFS()

class TestKittenFS(unittest.TestCase):
    # these need to be run in this order
    # master and worker in particular should be made before any other 
    # funs called
    def test_a_create_master(self):
        master = kitten.create_master()
        self.assertRegex(str(master), "<plyvel.DB with name '/tmp/cachedb/master'")
    def test_b_add_worker(self):
        worker = kitten.add_worker()
        self.assertRegex(str(worker), "<plyvel.DB with name '/tmp/cachedb/worker/0'")
    def test_c_put(self):
        result = kitten.put('A', 'hello')
        self.assertEqual(result, 'hello')
    def test_d_put(self):
        result = kitten.put('B', 'bye')
        self.assertEqual(result, 'bye')
    def test_e_get(self): 
        kitten.put('A', 'hello')
        result = kitten.get('A')
        self.assertEqual(result, 'hello'.encode())
    def test_f_delete(self):
        kitten.put('B', 'bye')
        result = kitten.delete('B', with_hash=False, is_testing=True)
        self.assertEqual(result, hashed_key('B').encode())
    def test_g_add_worker_to_master(self):
        meta_data = get_meta_data(kitten.worker_idx, 'A', 'bye')
        h_key = hashed_key(kitten.worker_idx)
        result = kitten.add_worker_to_master(str(h_key).encode(), str(meta_data).encode())
        self.assertEqual(str(h_key).encode(), result)
    def test_h_clear_worker(self):
        result = kitten.clear_worker(testing=True)
        self.assertEqual(result, "Cleared worker")
    def test_i_clear_master(self):
        result = kitten.clear_master()
        self.assertEqual(result, "Cleared master")
    def test_j_close_worker(self):
        result = kitten.close_worker()
        self.assertEqual(result, "closed worker " + str(kitten.worker_idx))
    def test_k_close_master(self):
        result = kitten.close_master()
        self.assertEqual(result, "closed master")

if __name__ == "__main__":
    unittest.main()
