import unittest
from main import get_city_datetime
from redis import Redis


class TestWorldTimes(unittest.TestCase):

    def test_redis(self):
        redis_client = Redis(host='localhost', port='6379')
        assert redis_client.ping()

    def test_city(self):
        utc_time = get_city_datetime('America/Belize')
        self.assertTrue('+00:00' in utc_time)


if __name__ == '__main__':
    unittest.main()
