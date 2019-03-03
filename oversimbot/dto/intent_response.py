
class IntentResponse:
    def __init__(self):
        self.key = ""
        self.entities={}

    def __str__(self):
        return str(self.__dict__)
