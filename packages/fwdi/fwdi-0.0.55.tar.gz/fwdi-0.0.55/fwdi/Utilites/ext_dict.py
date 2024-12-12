class ExtDict():
    @staticmethod
    def merge(a1:dict, a2:dict)->dict:
        a3 = dict(a1.items() | a2.items())
        return a3