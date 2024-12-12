import unittest

from src.toolkit.networking.address import get_local_ip


class AddressTestCase(unittest.TestCase):

    def test_get_local_ip(self):
        my_ip = get_local_ip()
        print(my_ip)
        self.assertIsNotNone(my_ip)


if __name__ == '__main__':
    unittest.main()
