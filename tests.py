import filecmp

from NFA_simulator import NFA_simulator
from NFA_to_DFA import NFA_to_DFA
from Virtual_mashine_regex import *
from DFA_minimize import *

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
    NFA_to_DFA("NFA1", "DFA_ANS_1")
    assert (NFA_simulator("NFA1", "0011100") == NFA_simulator("DFA_ANS_1", "0011100"))
    assert (NFA_simulator("NFA1", "000") == NFA_simulator("DFA_ANS_1", "000"))
    assert (NFA_simulator("NFA1", "0000") == NFA_simulator("DFA_ANS_1", "0000"))
    assert (NFA_simulator("NFA1", "110001111001001") == NFA_simulator("DFA_ANS_1", "110001111001001"))

    NFA_to_DFA("NFA2", "DFA_ANS_2")
    assert (NFA_simulator("NFA2", "0011100") == NFA_simulator("DFA_ANS_2", "0011100"))
    assert (NFA_simulator("NFA2", "0000000000") == NFA_simulator("DFA_ANS_2", "0000000000"))
    assert (NFA_simulator("NFA2", "101111000") == NFA_simulator("DFA_ANS_2", "101111000"))
    assert (NFA_simulator("NFA2", "110001111001101") == NFA_simulator("DFA_ANS_2", "110001111001101"))


def testRegex():
    pattern1 = build_pattern("a+b+")
    pattern2 = build_pattern("babab*a+")
    pattern3 = build_pattern("a*|b?")
    vm1 = Virtual_mashine_regex(pattern1)
    vm2 = Virtual_mashine_regex(pattern2)
    vm3 = Virtual_mashine_regex(pattern3)
    assert (vm1.run("aaaaaaa") == False)
    assert (vm1.run("bbbba") == False)
    assert (vm1.run("aaabbb") == True)
    assert (vm1.run("abbbbbbbbbb") == True)
    assert (vm1.run("ab") == True)

    assert (vm2.run("baba") == False)
    assert (vm2.run("babbbaaa") == False)
    assert (vm2.run("bababbb") == False)
    assert (vm2.run("babaaaa") == True)
    assert (vm2.run("bababbbbbbaaa") == True)

    assert (vm3.run("aaaaaab") == False)
    assert (vm3.run("bb") == False)
    assert (vm3.run("aaaaaaa") == True)
    assert (vm3.run("") == True)
    assert (vm3.run("b") == True)


def testMinimize():
    DFA_minimize("DFA1", "OUT1")
    DFA_minimize("DFA2", "OUT2")
    DFA_minimize("DFA3", "OUT3")
    assert (filecmp.cmp("OUT1", "DFA_ANS_1") == True)
    assert (filecmp.cmp("OUT2", "DFA_ANS_2") == True)
    assert (filecmp.cmp("OUT3", "DFA_ANS_3") == True)


def testAcceptAll():
    DFA_minimize("DFA1", "OUT1")
    DFA_minimize("DFA2", "OUT2")
    DFA_minimize("DFA3", "OUT3")
    assert (is_accept_all("OUT1") == False)
    assert (is_accept_all("OUT2") == False)
    assert (is_accept_all("OUT3") == True)

def testEq():
    assert (is_DFA_eq("DFA2", "DFA2") == True)
    assert (is_DFA_eq("DFA1", "DFA2") == False)
    assert (is_DFA_eq("DFA1", "DFA4") == True)
    assert (is_DFA_eq("DFA2", "DFA5") == True)