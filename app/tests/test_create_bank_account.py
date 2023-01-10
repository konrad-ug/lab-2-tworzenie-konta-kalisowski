import unittest
from ..Konto import Konto
from datetime import date
from unittest.mock import patch, MagicMock
from ..SMTP import SMTPConnection


class TestCreateBankAccount(unittest.TestCase):

    def test_tworzenie_konta(self):
        pierwsze_konto = Konto("Dariusz", "Januszewski", "01234567891")
        self.assertEqual(pierwsze_konto.imie, "Dariusz",
                         "Imie nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.nazwisko, "Januszewski",
                         "Nazwisko nie zostało zapisane!")
        self.assertEqual(pierwsze_konto.saldo, 0, "Saldo nie jest zerowe!")
        self.assertEqual(pierwsze_konto.pesel,
                         '01234567891', "Pesel nie został zapisany!")

    def test_tworzenie_kont2(self):
        drugie_konto = Konto("Dariusz", "Januszewski",
                             "0123456789", "PROM_331")
        self.assertEqual(drugie_konto.pesel,
                         "Niepoprawny pesel!", "Podano zły pesel")
        self.assertEqual(drugie_konto.prom, "PROM_331",
                         "Podano zły format kodu")

    def test_brak_promo(self):
        konto_brak_promo = Konto("Dariusz", "Januszewski",
                                 "0123456789")
        self.assertEqual(konto_brak_promo.prom, None,
                         "Konto nie powinno mieć domyślnie promo")

    def test_złykod_wiek_po60ur(self):
        konto_złykod_wiek_po60ur = Konto(
            "Jan", "Kowalski", "75021456785", "APROM_33")
        self.assertEqual(konto_złykod_wiek_po60ur.birth_check(), True,
                         "Wiek powinien być poprawny!")
        self.assertEqual(konto_złykod_wiek_po60ur.saldo, 0,
                         "Saldo powinno wynosić 0!")
        self.assertEqual(konto_złykod_wiek_po60ur.prom_check(),
                         0, "Saldo powinno wynosić 0")

    def test_złykod_wiek_zastary(self):
        konto_złykod_wiek_zastary = Konto(
            "Jan", "Kowalski", "52021456785", "APROM_33")
        self.assertEqual(konto_złykod_wiek_zastary.birth_check(), False,
                         "Wiek powinien być poprawny!")
        self.assertEqual(konto_złykod_wiek_zastary.saldo, 0,
                         "Saldo powinno wynosić 0!")
        self.assertEqual(konto_złykod_wiek_zastary.prom_check(),
                         0, "Saldo powinno wynosić 0")

    def test_kod_wiek_po60ur(self):
        konto_kod_wiek_po60ur = Konto(
            "Jan", "Kowalski", "75021456785", "PROM_332")
        self.assertEqual(konto_kod_wiek_po60ur.birth_check(), True,
                         "Wiek powinien być poprawny!")
        self.assertEqual(konto_kod_wiek_po60ur.saldo, 50,
                         "Saldo powinno wynosić 50!")
        self.assertEqual(konto_kod_wiek_po60ur.prom_check(),
                         50, "Saldo powinno wynosić 50")

    def test_kod_wiek_zastary(self):
        konto_kod_wiek_zastary = Konto(
            "Jan", "Kowalski", "52111461823", "PROM_332")
        self.assertEqual(konto_kod_wiek_zastary.prom, "PROM_332",
                         "Kod promocyjny nie został poprawnie wprowadzony")
        self.assertEqual(konto_kod_wiek_zastary.birth_check(), False,
                         "Wiek nie powinien być poprawny!")
        self.assertEqual(konto_kod_wiek_zastary.saldo,
                         0, "Saldo powinno wynosić 0!")
        self.assertEqual(konto_kod_wiek_zastary.prom_check(),
                         0, "Saldo powinno wynosić 0")


class BalanceOperations(unittest.TestCase):
    imie = "Dariusz"
    nazwisko = "Januszewski"
    pesel = "61092909876"

    def test_balance_decreases_transfer_out(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 500
        account.transfer_out(100)
        self.assertEqual(account.saldo, 500 - 100)

    def test_balance_increases_transfer_in(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 500
        account.transfer_in(100)
        self.assertEqual(account.saldo, 500 + 100)

    def test_balance_not_enough_transfer_out(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 50
        account.transfer_out(100)
        self.assertEqual(account.saldo, 50)

    def test_series_of_transfers(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 500
        account.transfer_in(100)
        account.transfer_out(100)
        account.transfer_in(10)
        self.assertEqual(account.saldo, 500 + 100 - 100 + 10)

    def test_series_of_transfers_express(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 500
        account.transfer_out_express(50)
        account.transfer_out_express(150)
        account.transfer_out_express(150)
        self.assertEqual(account.saldo, 500 - 51 - 151 - 151)

    def test_balance_enough_transfer_express(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 60
        account.transfer_out_express(50)
        self.assertEqual(account.saldo, 9)

    def test_balance_just_enough_transfer_express(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 50
        account.transfer_out_express(50)
        self.assertEqual(account.saldo, -1)

    def test_balance_not_enough_transfer_express(self):
        account = Konto(self.imie, self.nazwisko, self.pesel)
        account.saldo = 40
        account.transfer_out_express(50)
        self.assertEqual(account.saldo, 40)


class HistoryOperations(unittest.TestCase):
    name = "Dariusz"
    surname = "Januszewski"
    pesel = "01212567891"

    def test_history_new_account(self):
        account = Konto(self.name, self.surname, self.pesel)
        self.assertListEqual(
            account.history,
            [],
            "Historia transakcji nowego konta nie jest pusta!",
        )

    def test_history_transfer_in(self):
        account = Konto(self.name, self.surname, self.pesel)
        account.transfer_in(50)
        self.assertListEqual(
            account.history,
            [50],
            "Przelew przychodzący nie został dopisany do historii!",
        )

    def test_history_transfer_out(self):
        account = Konto(self.name, self.surname, self.pesel)
        account.saldo = 100
        account.transfer_out(50)
        self.assertListEqual(
            account.history,
            [-50],
            "Przelew wychodzący nie został dopisany do historii!",
        )

    def test_history_transfer_exrpress(self):
        account = Konto(self.name, self.surname, self.pesel)
        account.saldo = 100
        account.transfer_out_express(100)
        self.assertListEqual(
            account.history,
            [-100, -1],
            "Historia niepoprawna!",
        )

    def test_history_transfer_series(self):
        account = Konto(self.name, self.surname, self.pesel)
        account.saldo = 100
        account.transfer_out(50)
        account.transfer_in(50)
        account.transfer_out_express(50)
        self.assertListEqual(
            account.history,
            [-50, 50, -50, -1],
            "Historia niepoprawna!",
        )


class EmailSending(unittest.TestCase):
    name = "Dariusz"
    surname = "Januszewski"
    pesel = "01212567891"

    def test_success_sending_email_with_history(self):
        account = Konto(self.name, self.surname, self.pesel)
        account.saldo = 100
        account.transfer_out(50)
        account.transfer_in(50)
        smtp = SMTPConnection()
        smtp.wyslij = MagicMock(return_value=True)
        state = account.wyslij_historie_na_maila("testemail@test.com", smtp)
        self.assertEqual(state, True, "Wysyłanie maila nie powiodło się!")
        smtp.wyslij.assert_called_once_with(
            f"Wyciag z dnia {date.today()}", f"Twoja historia konta to: {account.history}", "testemail@test.com")

    def test_fail_sending_email_with_history(self):
        account = Konto(self.name, self.surname, self.pesel)
        account.saldo = 100
        account.transfer_out(50)
        account.transfer_in(50)
        smtp = SMTPConnection()
        smtp.wyslij = MagicMock(return_value=False)
        state = account.wyslij_historie_na_maila("testemail@test.com", smtp)
        self.assertEqual(state, False, "Wysyłanie maila nie powiodło się!")
        smtp.wyslij.assert_called_once_with(
            f"Wyciag z dnia {date.today()}", f"Twoja historia konta to: {account.history}", "testemail@test.com")
