import unittest

class TestUtil(unittest.TestCase):
    def test_point_to_tile_fraction(self):
        from tilepack.util import point_to_tile_fraction

        self.assertEqual(
            point_to_tile_fraction(0, 0, 10),
            [512.0, 512.0, 10]
        )

        self.assertEqual(
            point_to_tile_fraction(-122.2712, 37.8043, 10),
            [164.2063644444445, 395.6916183248187, 10]
        )

    def test_point_to_tile(self):
        from tilepack.util import point_to_tile

        self.assertEqual(
            point_to_tile(0, 0, 10),
            [512, 512, 10]
        )
        self.assertEqual(
            point_to_tile(-122.2712, 37.8043, 10),
            [164, 395, 10]
        )
