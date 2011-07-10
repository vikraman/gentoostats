
import unittest
from app import app

class TestIndex(unittest.TestCase):

    def setUp(self):
        self.b = app.browser()
        self.b.open('/')

    def test_basic(self):
        self.assertEqual(self.b.path, '/')
        self.assertEqual(self.b.status, 200)

    def test_content(self):
        self.assertTrue('Welcome to the gentoostats webapp' in self.b.data)

    def test_hosts(self):
        self.assertTrue('Number of hosts' in self.b.data)
        lines = self.b.data.split('\n')
        for line in lines:
            if line.startswith('Number of hosts'):
                words = line.split()
                count = int(words[-1].strip('</br>'))
                self.assertGreaterEqual(count, 0)
                break
