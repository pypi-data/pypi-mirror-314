import unittest

from juham_visualcrossing.visualcrossing import VisualCrossing


class TestVisualCrossing(unittest.TestCase):
    """Unit tests for `VisualCrossing` weather forecast masterpiece."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = VisualCrossing.get_class_id()
        self.assertEqual("VisualCrossing", classid)


if __name__ == "__main__":
    unittest.main()
