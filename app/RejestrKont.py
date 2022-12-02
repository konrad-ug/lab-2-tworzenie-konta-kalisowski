class RejestrKont():
    users = []

    @classmethod
    def addUser(cls, user):
        cls.users.append(user)

    @classmethod
    def searchUser(cls, pesel):
        for user in cls.users:
            if user.pesel == pesel:
                return user
        return None

    @classmethod
    def updateUser(cls, pesel, data):
        user = cls.searchUser(pesel)
        if data.get('imie'):
            user.imie = data['imie']
        if data.get('nazwisko'):
            user.nazwisko = data['nazwisko']
        if data.get('pesel'):
            user.pesel = data['pesel']
        if data.get('saldo'):
            user.saldo = data['saldo']
        return user, 200

    @classmethod
    def usersCount(cls):
        return len(cls.users)

    @classmethod
    def deleteUser(cls, pesel):
        for user in cls.users:
            if user.pesel == pesel:
                cls.users.remove(user)
                return "user deleted"
        return None
