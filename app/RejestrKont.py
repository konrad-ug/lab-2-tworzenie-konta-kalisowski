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
    def usersCount(cls):
        return len(cls.users)
