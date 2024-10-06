from NFA_simulator import NFA_simulator
from NFA_to_DFA import NFA_to_DFA


def testsSimulator():
    assert (NFA_simulator("NFA1", "0011100") == True)
    assert (NFA_simulator("NFA1", "000") == True)
    assert (NFA_simulator("NFA1", "101111000") == False)
    assert (NFA_simulator("NFA1", "110001111001001") == False)

    assert (NFA_simulator("NFA2", "0011100") == False)
    assert (NFA_simulator("NFA2", "000000") == True)
    assert (NFA_simulator("NFA2", "101111000") == True)
    assert (NFA_simulator("NFA2", "110001111001101") == False)


def testsConvert():
    NFA_to_DFA("NFA1", "DFA1")
    assert (NFA_simulator("NFA1", "0011100") == NFA_simulator("DFA1", "0011100"))
    assert (NFA_simulator("NFA1", "000") == NFA_simulator("DFA1", "000"))
    assert (NFA_simulator("NFA1", "0000") == NFA_simulator("DFA1", "0000"))
    assert (NFA_simulator("NFA1", "110001111001001") == NFA_simulator("DFA1", "110001111001001"))

    NFA_to_DFA("NFA2", "DFA2")
    assert (NFA_simulator("NFA2", "0011100") == NFA_simulator("DFA2", "0011100"))
    assert (NFA_simulator("NFA2", "0000000000") == NFA_simulator("DFA2", "0000000000"))
    assert (NFA_simulator("NFA2", "101111000") == NFA_simulator("DFA2", "101111000"))
    assert (NFA_simulator("NFA2", "110001111001101") == NFA_simulator("DFA2", "110001111001101"))