from NightPy.nightpy import NightPy

class Client:
    def __init__(self):
        self.np = NightPy(self.get_token())

    def get_token(self):
        pass

