from compound import *
from compound.i.iAc import *
from compound.i.iSa import *
from element import get_me_oxs, is_me_activer
from reaction import *
from tools.comps import simple

def r_1(comps: 'list(Compound)', is_input):
    """`iSiMe + `HNO3` -> `iSaNo + `NO2` + `iWa"""
    react: str

    if is_input:
        iSiMe = Compound("Cu")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiMe = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        if me in ["Au", "Pt"]:
            return ""
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + NO2 + H2O"
    else:
        iSaNo = Compound("Cu(NO3)2")
        if len(comps) == 1:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
        elif len(comps) == 2:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
        else:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
            else:
                iSaNo = comps[2]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an != "NO3":
            return ""
        if me in ["Au", "Pt"]:
            return ""

        iSiMe = Compound(simple(me))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + NO2 + H2O"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """`iSiMe + `HNO3` -> `iSaNo + `NO` + `iWa"""
    react: str

    if is_input:
        iSiMe = Compound("Ni")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiMe = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        if me in ["Au", "Pt"]:
            return ""
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + NO + H2O"
    else:
        iSaNo = Compound("Ni(NO3)2")
        if len(comps) == 1:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
        elif len(comps) == 2:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
        else:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
            else:
                iSaNo = comps[2]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an != "NO3":
            return ""
        if me in ["Au", "Pt"]:
            return ""

        iSiMe = Compound(simple(me))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + NO + H2O"

    return Reaction(react)

def r_3(comps: 'list(Compound)', is_input):
    """`iSiMe + `HNO3` -> `iSaNo + `N2O` + `iWa"""
    react: str

    if is_input:
        iSiMe = Compound("Zn")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiMe = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        if me in ["Au", "Pt"]:
            return ""
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + N2O + H2O"
    else:
        iSaNo = Compound("Zn(NO3)2")
        if len(comps) == 1:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
        elif len(comps) == 2:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
        else:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
            else:
                iSaNo = comps[2]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an != "NO3":
            return ""
        if me in ["Au", "Pt"]:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSiMe = Compound(simple(me))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + N2O + H2O"

    return Reaction(react)

def r_4(comps: 'list(Compound)', is_input):
    """`iSiMe + `HNO3` -> `iSaNo + `N2` + `iWa"""
    react: str

    if is_input:
        iSiMe = Compound("Al")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiMe = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        if me in ["Au", "Pt"]:
            return ""
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + N2 + H2O"
    else:
        iSaNo = Compound("Al(NO3)3")
        if len(comps) == 1:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
        elif len(comps) == 2:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
        else:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
            else:
                iSaNo = comps[2]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an != "NO3":
            return ""
        if me in ["Au", "Pt"]:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSiMe = Compound(simple(me))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + N2 + H2O"

    return Reaction(react)

def r_5(comps: 'list(Compound)', is_input):
    """`iSiMe + `HNO3` -> `iSaNo + `AmmNO3` + `iWa"""
    react: str

    if is_input:
        iSiMe = Compound("Mg")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiMe = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        if me in ["Au", "Pt"]:
            return ""
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + AmmNO3 + H2O"
    else:
        iSaNo = Compound("Mg(NO3)2")
        if len(comps) == 1:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
        elif len(comps) == 2:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
        else:
            if "iSaNo" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSaNo" in comps[1].comp_type:
                iSaNo = comps[1]
            else:
                iSaNo = comps[2]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an != "NO3":
            return ""
        if me in ["Au", "Pt"]:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSiMe = Compound(simple(me))

        react = f"{iSiMe} + HNO3 -> {iSaNo} + AmmNO3 + H2O"

    return Reaction(react)
