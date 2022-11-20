from decimal import Clamped
import imp
from app.Konto import Konto


class Konto_firmowe(Konto):
    def __init__(self, nip, nazwa_firmy):
        self.nip = self.nip_check(nip)
        self.nazwa_firmy = nazwa_firmy
        self.saldo = 0
        self.history = []

    def nip_check(self, pesel):
        if (len(pesel) != 10):
            return "Niepoprawny NIP!"
        else:
            return pesel

    def transfer_out_express_buisness(self, x):
        if (self.saldo >= x):
            self.saldo -= x + 5
            self.history.extend([-x, -5])

    def check_credit_zus(self):
        check = False
        for x in self.history:
            if (x == -1775):
                check = True
        return check

    def zaciagnij_kredyt(self, kwota):
        if (self.check_credit_zus() and self.saldo >= kwota * 2):
            self.saldo += kwota
            return True
        return False
