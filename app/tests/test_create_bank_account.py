import unittest
from ..Konto import Konto


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
