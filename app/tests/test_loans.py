import unittest
from parameterized import parameterized
from app.Konto import Konto


class TestLoans(unittest.TestCase):
    def setUp(self):
        self.konto = Konto("Mariusz", "Pudzianowski", "01321007158")

    @parameterized.expand([
        ([100, 100, 100, 400, 500], 500, True, 500),
        ([-100, 100, 100, -100], 500, False, 0),
        ([100, -100, 100, 200, 500], 500, True, 500),
        ([-1000], 20, False, 0),
        ([-50, -100, 100, 150, -300], 500, False, 0),
        ([500, 200], 500, False, 0),

    ])
    def test_loan(self, history, sum, output, balance):
        self.konto.history = history
        test = self.konto.zaciagnij_kredyt(sum)
        self.assertEqual(test, output)
        self.assertEqual(self.konto.saldo, balance)
