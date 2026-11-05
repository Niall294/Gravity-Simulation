import unittest
from gravity_simulation import *

class TestCalculator(unittest.TestCase): # only preserves the angle within the quadrant
    def test_direction_atan(self): # preserves the whole angle including the quadrant
        direction = math.atan2((0 - 10), (0 - 10))
        self.assertEqual(direction, -0.7853981633974483)

if __name__ == '__main__':
    unittest.main()