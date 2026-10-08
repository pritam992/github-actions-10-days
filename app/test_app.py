import unittest
from app import response


class AppTests(unittest.TestCase):
    def test_health(self):
        self.assertEqual(response('/health'), (200, {'status': 'ok'}))

    def test_home(self):
        status, body = response('/')
        self.assertEqual(status, 200)
        self.assertIn('message', body)

    def test_unknown_path(self):
        self.assertEqual(response('/missing')[0], 404)


if __name__ == '__main__':
    unittest.main()
