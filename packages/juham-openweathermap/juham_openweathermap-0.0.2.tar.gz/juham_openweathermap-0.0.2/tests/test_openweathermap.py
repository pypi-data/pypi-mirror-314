import unittest

from juham_openweathermap.openweathermap import OpenWeatherMap


class TestOpenWeatherMap(unittest.TestCase):
    """Unit tests for `OpenWeatherMap` weather forecast masterpiece."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = OpenWeatherMap.get_class_id()
        self.assertEqual("OpenWeatherMap", classid)


if __name__ == "__main__":
    unittest.main()
