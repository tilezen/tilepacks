import unittest

class TestBuilder(unittest.TestCase):
    def test_cover_bbox(self):
        from tilepack.builder import cover_bbox

        self.assertEqual(
            list(cover_bbox(-93.55957, 38.13456, -82.30957, 45.24395, 5)),
            [
                (7, 11, 5),
                (7, 12, 5),
                (8, 11, 5),
                (8, 12, 5),
            ]
        )

        self.assertEqual(
            list(cover_bbox(-74.501, 40.345, -73.226, 41.097, 5)),
            [
                (9, 11, 5),
                (9, 12, 5),
            ]
        )
