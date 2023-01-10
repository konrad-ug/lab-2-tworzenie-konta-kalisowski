from app.Konto import Konto
from datetime import date
import requests
import os
from dotenv import load_dotenv
load_dotenv()


class Konto_firmowe(Konto):
    def __init__(self, nip, nazwa_firmy):
        self.nip = self.nip_check(nip)
        self.nazwa_firmy = nazwa_firmy
        self.saldo = 0
        self.history = []

    def nip_check(self, nip):
        if (len(nip) != 10):
            return "Niepoprawny NIP!"
        else:
            if self.nip_real_check(nip):
                return nip
            else:
                return "Pranie!"

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

    def nip_real_check(self, nip):
        date_today = date.today()
        url = os.environ.get("BANK_APP_MF_URL")
        res = requests.get(f'{url}{nip}?date={date_today}')
        if res.status_code == 200:
            return True
        return False

    def zaciagnij_kredyt(self, kwota):
        if (self.check_credit_zus() and self.saldo >= kwota * 2):
            self.saldo += kwota
            return True
        return False

    def wyslij_historie_na_maila(self, email, smtp):
        topic = f"Wyciag z dnia {date.today()}"
        body = f"Historia konta Twojej firmy to: {self.history}"
        return smtp.wyslij(topic, body, email)
