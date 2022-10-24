import unittest
import re
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
        print(drugie_konto.saldo)
        self.assertEqual(drugie_konto.pesel,
                         "Niepoprawny pesel!", "Podano zły pesel")
        self.assertEqual(drugie_konto.prom, "PROM_331", "Podano zły format")

    def test_brak_promo(self):
        drugie_konto = Konto("Dariusz", "Januszewski",
                             "0123456789")
        self.assertEqual(drugie_konto.prom, None, "Podano zły format")

    def test_kod_zbyt_stary(self):
        konto_za_stary = Konto(
            "Jan", "Kowalski", "52111461823", "PROM_332")
        print(konto_za_stary.birth_check())
        self.assertEqual(konto_za_stary.birth_check(), False)
