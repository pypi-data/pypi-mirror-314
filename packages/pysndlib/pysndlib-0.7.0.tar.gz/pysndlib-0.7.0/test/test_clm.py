import unittest
import pysndlib.clm as clm

class CLMGeneratorsTest(unittest.TestCase):
    def test_is_all_pass(self):
        self.assertTrue(clm.is_all_pass(clm.make_all_pass(.5, .5, 100)))
        self.assertFalse(clm.is_all_pass(clm.make_oscil(440.)))
    def test_make_all_pass(self):
        self.assertIsInstance(clm.make_all_pass(.5, .5, 100), clm.mus_any)
    def test_all_pass(self):
        gen = clm.make_all_pass(.5, .5, 100)
        self.assertEqual(clm.all_pass(gen, 0.0), 0.0)
        self.assertEqual(clm.all_pass(gen, 1.0), .5)
        self.assertEqual(clm.all_pass(gen, -1.0), -.5)

        

if __name__ == '__main__':
    unittest.main()
    
    
