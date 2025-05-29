from enum import Enum


class States(Enum):
    WA = 1
    NT = 2
    Q = 3
    NSW = 4
    V = 5
    SA = 6
    T = 7

    def __lt__(self, other):
        if type(other) != type(self):
            return False

        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        return self.value == other.value

    def __hash__(self):
        return hash(repr(self))


class SAStates(Enum):
    ARG = 1
    BOL = 2
    BRA = 3
    CHI = 4
    COL = 5
    ECU = 6
    GUY = 7
    PAR = 8
    PER = 9
    SUR = 10
    URU = 11
    VEN = 12

    def __lt__(self, other):
        if type(other) != type(self):
            return False
        return self.value < other.value

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return self.value == other.value

    def __hash__(self):
        return hash(repr(self))
