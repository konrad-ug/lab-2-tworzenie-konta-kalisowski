class Konto:
    def __init__(self, imie, nazwisko, pesel, prom=None):
        self.imie = imie
        self.nazwisko = nazwisko
        self.pesel = self.pesel_check(pesel)
        self.prom = prom
        self.saldo = self.prom_check()
        self.history = []

    def pesel_check(self, pesel):
        if (len(pesel) != 11):
            return "Niepoprawny pesel!"
        else:
            return pesel

    def prom_check(self):
        if self.birth_check() and self.prom != None:
            if len(self.prom) == 8:
                if self.prom[0:5] == "PROM_":
                    return 50
        return 0

    def birth_check(self):
        pesel = self.pesel
        if pesel != "Niepoprawny pesel!":
            if (int(pesel[2]) > 1 or (int(pesel[0]) >= 6 and int(pesel[2]) < 2)):
                return True
        return False

    def transfer_in(self, x):
        self.saldo += x
        self.history.append(x)

    def transfer_out(self, x):
        if (self.saldo >= x):
            self.saldo -= x
            self.history.append(-x)

    def transfer_out_express(self, x):
        if (self.saldo >= x):
            self.saldo -= x + 1
            self.history.extend([-x, -1])
