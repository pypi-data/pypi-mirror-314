import unittest
import wangph

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(wangph.math.np_plus(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(wangph.math.np_minus(2, 1), 1)

    def test_multiply(self):
        self.assertEqual(wangph.math.np_mul(2, 3), 6)

    def test_divide(self):
        self.assertEqual(wangph.math.np_div(6, 3), 2)

if __name__ == '__main__':
    unittest.main()