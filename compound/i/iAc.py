from copy import deepcopy

from element import Element
from tools.comps import index
from tools.container import find_if
from database.compounds.iAc import db_acid_react

# return (anion, oxs) via acid
def iAc_oxs(comp: 'Formula') -> (str, int):
    val = comp.value.replace('[', "").replace(']', "")

    consist = deepcopy(comp.consist) # ElAn
    an_oxs = consist[Element("H")]

    end = val[1 : ]
    anion = ""

    anion = end[find_if(end, lambda x: x.isupper()) : ]
    if '[' in comp.value:
        anion = '[' + anion + ']'
    return (anion, int(an_oxs))

# return (element, oxs) via acid
def iAc_el_oxs(comp: 'Formula') -> (str, int):
    consist = deepcopy(comp.consist) # HElO || HEl
    h_q = consist[Element("H")]
    del consist[Element("H")] # ElO || El

    o_q = 0
    if Element("O") in consist:
        o_q = consist[Element("O")]
        del consist[Element("O")] # El

    x = list(consist.keys())[0]
    x_q = consist[x]
    x_oxs = (o_q * 2 - h_q) / x_q

    return (x.name, int(abs(x_oxs)))

# return acid via (anion, oxs)
def iAc_create(an: str, an_oxs: int) -> (str): # H{an_oxs}An
    iAc = "H" + index(an_oxs) + an
    return iAc

# return acid with oxygen via (element, oxs)
def iAc_el_create(x: str, x_oxs: int) -> (str): # H{h_q}ElO{o_q}
    if x == "P" and x_oxs == 5:
        return "H3PO4"

    h_q = 1 + (x_oxs + 1) % 2
    o_q = int((h_q + x_oxs) / 2)

    iAc = "H" + index(h_q) + x + "O" + index(o_q)
    return iAc

# check is acid #1 activer than acid #2
def is_iAc_activer(ac1: str, ac2: str):
    if ac1 in ["HCl", "HNO3", "H3PO4"]:
        if ac2 in ["HCl", "HNO3", "H3PO4"]:
            return False
    f1 = 0
    if ac1 in db_acid_react:
        f1 = db_acid_react.index(ac1)
    else:
        if not is_iAc_activer(ac2, "H2SO3"):
            return True
        else:
            return False
    f2 = 0
    if ac2 in db_acid_react:
        f2 = db_acid_react.index(ac2)
    else:
        if is_iAc_activer(ac1, "H2SO3"):
            return True
        else:
            return False
    return f1 < f2
