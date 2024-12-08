import unittest

from masterpiece_plugin import HelloWorld


class TestHelloWorld(unittest.TestCase):
    """Unit tests for `HelloWorld` class."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = HelloWorld.get_class_id()
        self.assertEqual("HelloWorld", classid)


if __name__ == "__main__":
    unittest.main()
