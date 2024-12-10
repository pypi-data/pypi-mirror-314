import unittest
import tellurium as te
from tmodelviz.simulator import load_and_simulate

class TestLoadAndSimulate(unittest.TestCase):

    def setUp(self):
        self.url = 'https://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000297'
        self.start_time = 0
        self.end_time = 10
        self.steps = 100

    def test_load_and_simulate(self):
        runner, data = load_and_simulate(self.url, self.start_time, self.end_time, self.steps)
        self.assertIsNotNone(runner)
        self.assertIsNotNone(data)
        self.assertEqual(len(data), self.steps + 1)

    def test_invalid_url(self):
        with self.assertRaises(Exception):
            load_and_simulate('invalid_url', self.start_time, self.end_time, self.steps)

if __name__ == '__main__':
    unittest.main()