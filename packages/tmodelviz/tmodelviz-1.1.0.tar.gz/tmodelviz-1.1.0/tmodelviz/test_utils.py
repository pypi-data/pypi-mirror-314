import unittest
import numpy as np
from tmodelviz.utils import calculate_rolling_average, extract_fluxes

class TestUtils(unittest.TestCase):

    def test_calculate_rolling_average(self):
        concentrations = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        time = np.arange(10)
        index = 5
        window_size = 3
        result = calculate_rolling_average(concentrations, time, index, window_size)
        expected = np.mean([4, 5, 6])
        self.assertEqual(result, expected)

        index = 0
        result = calculate_rolling_average(concentrations, time, index, window_size)
        expected = np.mean([1, 2])
        self.assertEqual(result, expected)

        index = 9
        result = calculate_rolling_average(concentrations, time, index, window_size)
        expected = np.mean([9, 10])
        self.assertEqual(result, expected)

    def test_extract_fluxes(self):
        class MockRunner:
            def __init__(self):
                self.data = {}
            def reset(self):
                self.data = {}
            def __setitem__(self, key, value):
                self.data[key] = value
            def getReactionRates(self):
                return [self.data[species] * 2 for species in self.data]
            def getReactionIds(self):
                return list(self.data.keys())

        runner = MockRunner()
        species_names = ['A', 'B', 'C']
        species_concentrations = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ])
        index = 1
        rates, ids = extract_fluxes(runner, species_names, species_concentrations, index)
        self.assertEqual(rates, [8, 10, 12])
        self.assertEqual(ids, ['A', 'B', 'C'])

if __name__ == '__main__':
    unittest.main()