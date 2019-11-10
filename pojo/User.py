class User:
    __phone = None
    __password = None

    def __init__(self, phone, password):
        self.__phone = phone
        self.__password = password
        return

    def setPhone(self, phone):
        self.__phone = phone
        return

    def setPassword(self, password):
        self.__password = password
        return

    def getPhone(self):
        return self.__phone

    def getPassword(self):
        return self.__password
