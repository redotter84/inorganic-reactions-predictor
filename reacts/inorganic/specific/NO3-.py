from compound import *
from compound.i.iOx import *
from compound.i.iSa import *
from element import get_me_oxs, is_me_activer
from reaction import *
from tools.comps import simple

def r_1(comps: 'list(Compound)', is_input):
    """`iSaNo -> `iSaNo + `O2`"""
    react: str

    if is_input:
        iSaNO3 = comps[0]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNO3.formula)
        if an != "NO3":
            return ""
        if is_me_activer("Na", 1, me, me_oxs):
            return ""

        iSaNO2 = Compound(iSaNo_create(me, me_oxs, "NO2", 1))

        react = f"{iSaNO3} -> {iSaNO2} + O2"
    else:
        iSaNO2 = Compound("NaNO2")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNO2 = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNO2 = comps[0]
            else:
                iSaNO2 = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNO2.formula)
        if an != "NO2":
            return ""
        if is_me_activer("Na", 1, me, me_oxs):
            return ""

        iSaNO3 = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSaNO3} -> {iSaNO2} + O2"

    return Reaction(react, "t ")

def r_2(comps: 'list(Compound)', is_input):
    """`iSaNo -> (`iOxBa_, `iOxAm_) + `NO2` + `O2`"""
    react: str

    if is_input:
        iSaNO3 = comps[0]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNO3.formula)
        if an != "NO3":
            return ""
        if not is_me_activer("Na", 1, me, me_oxs) or me == "Na":
            return ""
        if is_me_activer("Cu", 2, me, me_oxs):
            return ""

        iOxBa = Compound(iOx_create(me, me_oxs))

        react = f"{iSaNO3} -> {iOxBa} + NO2 + O2"
    else:
        iOxBa = Compound("CuO")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
        elif len(comps) == 2:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
            elif "iOx" in comps[0].comp_type:
                iOxBa = comps[1]
        else:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
            elif "iOx" in comps[1].comp_type:
                iOxBa = comps[1]
            else:
                iOxBa = comps[2]

        if iOxBa.formula.value == "NO2":
            iOxBa = Compound("CuO")

        (me, me_oxs) = iOx_oxs(iOxBa.formula)
        if not is_me_activer("Na", 1, me, me_oxs) or me == "Na":
            return ""
        if is_me_activer("Cu", 2, me, me_oxs):
            return ""

        iSaNO3 = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSaNO3} -> {iOxBa} + NO2 + O2"

    return Reaction(react, "t ")

def r_3(comps: 'list(Compound)', is_input):
    """`iSaNo -> `iSiMe + `NO2` + `O2`"""
    react: str

    if is_input:
        iSaNO3 = comps[0]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNO3.formula)
        if an != "NO3":
            return ""
        if is_me_activer(me, me_oxs, "Cu", 2) or me == "Cu":
            return ""

        iSiMe = Compound(simple(me))

        react = f"{iSaNO3} -> {iSiMe} + NO2 + O2"
    else:
        iSiMe = Compound("Ag")
        if len(comps) == 1:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
        elif len(comps) == 2:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
            elif "iSiMe" in comps[1].comp_type:
                iSiMe = comps[1]
        else:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
            elif "iSiMe" in comps[1].comp_type:
                iSiMe = comps[1]
            else:
                iSiMe = comps[2]

        me = list(iSiMe.formula.consist.keys())[0].name
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer(me, me_oxs, "Cu", 2) or me == "Cu":
            return ""

        iSaNO3 = Compound(iSaNo_create(me, me_oxs, "NO3", 1))

        react = f"{iSaNO3} -> {iSiMe} + NO2 + O2"

    return Reaction(react, "t ")
