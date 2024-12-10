import unittest
import tellurium as te
from tmodelviz.simulator import load_and_simulate

class TestLoadAndSimulate(unittest.TestCase):

    def setUp(self):
        # Set up the test case with initial parameters
        self.url = 'https://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000297'
        self.start_time = 0
        self.end_time = 10
        self.steps = 100

    def test_load_and_simulate(self):
        # Test the load_and_simulate function with valid parameters
        runner, data = load_and_simulate(self.url, self.start_time, self.end_time, self.steps)
        self.assertIsNotNone(runner)  # Check that the runner is not None
        self.assertIsNotNone(data)    # Check that the data is not None
        self.assertEqual(len(data), self.steps + 1)  # Check that the data length is correct

    def test_invalid_url(self):
        # Test the load_and_simulate function with an invalid URL
        with self.assertRaises(Exception):  # Expect an exception to be raised
            load_and_simulate('invalid_url', self.start_time, self.end_time, self.steps)

if __name__ == '__main__':
    # Run the unit tests
    unittest.main()