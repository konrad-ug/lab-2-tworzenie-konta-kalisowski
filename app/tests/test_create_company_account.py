import unittest
from app.Konto_firmowe import Konto_firmowe
from unittest.mock import patch, Mock


class TestCreateCompanyAccount(unittest.TestCase):
    nip = "0123456789"
    nip_bad = "123456789"
    nazwa_firmy = "Tesla"

    def _mock_response(self, status):
        return Mock(status_code=status)

    @patch('requests.get')
    def test_nip_doesnt_exist(self, mock_get):
        mock_res = self._mock_response(status=400)
        mock_get.return_value = mock_res
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        self.assertEqual(account.nip, "Pranie!")

    @patch('requests.get')
    def test_nip_correct(self, mock_get):
        mock_res = self._mock_response(status=200)
        mock_get.return_value = mock_res
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        self.assertEqual(account.nip, "0123456789")

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_credidentials_are_correct(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        self.assertEqual(account.saldo, 0)
        self.assertEqual(account.nazwa_firmy, "Tesla")
        self.assertEqual(account.nip, "0123456789")

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_nip_incorrect(self, mock_nip_real_check):
        mock_nip_real_check.return_value = False
        account = Konto_firmowe(self.nip_bad, self.nazwa_firmy)
        self.assertEqual(account.nip, "Niepoprawny NIP!")

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_balance_decreases_transfer_out(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_out(100)
        self.assertEqual(account.saldo, 500 - 100)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_balance_increases_transfer_in(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_in(100)
        self.assertEqual(account.saldo, 500 + 100)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_balance_not_enough_transfer_out(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 50
        account.transfer_out(100)
        self.assertEqual(account.saldo, 50)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_series_of_transfers(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_in(100)
        account.transfer_out(100)
        account.transfer_in(10)
        self.assertEqual(account.saldo, 500 + 100 - 100 + 10)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_series_of_transfers_express(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_out_express_buisness(50)
        account.transfer_out_express_buisness(150)
        account.transfer_out_express_buisness(150)
        self.assertEqual(account.saldo, 500 - 55 - 155 - 155)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_balance_enough_transfer_express_buisness(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 60
        account.transfer_out_express_buisness(50)
        self.assertEqual(account.saldo, 5)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_balance_just_enough_transfer_express_buisness(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 50
        account.transfer_out_express_buisness(50)
        self.assertEqual(account.saldo, -5)

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_balance_not_enough_transfer_express_buisness(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 40
        account.transfer_out_express_buisness(50)
        self.assertEqual(account.saldo, 40)


class HistoryOperationsCompany(unittest.TestCase):
    nip = "0123456789"
    nazwa_firmy = "Tesla"

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_company_history_new_account(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        self.assertListEqual(
            account.history,
            [],
            "Historia transakcji nowego konta biznesowego nie jest pusta!",
        )

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_company_history_transfer_in(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.transfer_in(50)
        self.assertListEqual(
            account.history,
            [50],
            "Przelew przychodzący nie został dopisany do historii!",
        )

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_company_history_transfer_out(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 100
        account.transfer_out(50)
        self.assertListEqual(
            account.history,
            [-50],
            "Przelew wychodzący nie został dopisany do historii!",
        )

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_company_history_transfer_exrpress(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 100
        account.transfer_out_express_buisness(100)
        self.assertListEqual(
            account.history,
            [-100, -5],
            "Historia niepoprawna!",
        )

    @ patch('app.Konto_firmowe.Konto_firmowe.nip_real_check')
    def test_company_history_transfer_series(self, mock_nip_real_check):
        mock_nip_real_check.return_value = True
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 100
        account.transfer_out(50)
        account.transfer_in(50)
        account.transfer_out_express_buisness(50)
        self.assertListEqual(
            account.history,
            [-50, 50, -50, -5],
            "Historia niepoprawna!",
        )
