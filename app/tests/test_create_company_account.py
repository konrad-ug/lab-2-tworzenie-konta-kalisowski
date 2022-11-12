import unittest
from app.Konto_firmowe import Konto_firmowe


class TestCreateCompanyAccount(unittest.TestCase):
    nip = "0123456789"
    nip_bad = "123456789"
    nazwa_firmy = "Tesla"

    def test_credidentials_are_correct(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        self.assertEqual(account.saldo, 0)
        self.assertEqual(account.nazwa_firmy, "Tesla")
        self.assertEqual(account.nip, "0123456789")

    def test_nip_incorrect(self):
        account = Konto_firmowe(self.nip_bad, self.nazwa_firmy)
        self.assertEqual(account.nip, "Niepoprawny NIP!")

    def test_balance_decreases_transfer_out(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_out(100)
        self.assertEqual(account.saldo, 500 - 100)

    def test_balance_increases_transfer_in(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_in(100)
        self.assertEqual(account.saldo, 500 + 100)

    def test_balance_not_enough_transfer_out(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 50
        account.transfer_out(100)
        self.assertEqual(account.saldo, 50)

    def test_series_of_transfers(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_in(100)
        account.transfer_out(100)
        account.transfer_in(10)
        self.assertEqual(account.saldo, 500 + 100 - 100 + 10)

    def test_series_of_transfers_express(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 500
        account.transfer_out_express_buisness(50)
        account.transfer_out_express_buisness(150)
        account.transfer_out_express_buisness(150)
        self.assertEqual(account.saldo, 500 - 55 - 155 - 155)

    def test_balance_enough_transfer_express_buisness(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 60
        account.transfer_out_express_buisness(50)
        self.assertEqual(account.saldo, 5)

    def test_balance_just_enough_transfer_express_buisness(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 50
        account.transfer_out_express_buisness(50)
        self.assertEqual(account.saldo, -5)

    def test_balance_not_enough_transfer_express_buisness(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 40
        account.transfer_out_express_buisness(50)
        self.assertEqual(account.saldo, 40)


class HistoryOperationsCompany(unittest.TestCase):
    nip = "0123456789"
    nazwa_firmy = "Tesla"

    def test_company_history_new_account(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        self.assertListEqual(
            account.history,
            [],
            "Historia transakcji nowego konta biznesowego nie jest pusta!",
        )

    def test_company_history_transfer_in(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.transfer_in(50)
        self.assertListEqual(
            account.history,
            [50],
            "Przelew przychodzący nie został dopisany do historii!",
        )

    def test_company_history_transfer_out(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 100
        account.transfer_out(50)
        self.assertListEqual(
            account.history,
            [-50],
            "Przelew wychodzący nie został dopisany do historii!",
        )

    def test_company_history_transfer_exrpress(self):
        account = Konto_firmowe(self.nip, self.nazwa_firmy)
        account.saldo = 100
        account.transfer_out_express_buisness(100)
        self.assertListEqual(
            account.history,
            [-100, -5],
            "Historia niepoprawna!",
        )

    def test_company_history_transfer_series(self):
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
