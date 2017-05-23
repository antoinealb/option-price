import unittest
from price_option import volatility
from math import sqrt

class VolatilityTest(unittest.TestCase):
    def test_estimate(self):
        """
        Checks we can estimate the data using the examples from
        https://www.fool.com/knowledge-center/how-to-calculate-annualized-volatility.aspx
        """
        data = [
            1972.18, 1988.87, 1987.6, 1940.51, 1867.61, 1839.21, 1970.89,
            2035.73, 2079.61, 2096.92, 2102.44, 2091.54, 2083.39, 2086.05,
            2084.07, 2104.18, 2077.57, 2083.56, 2099.84, 2099.32, 2098.04
        ]

        v = volatility(data)

        self.assertAlmostEqual(0.0213 * sqrt(len(data)), v, 2)
