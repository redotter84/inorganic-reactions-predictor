from compound import *
from compound.i.iAc import *
from compound.o.oH import *
from compound.o.oHal import *
from compound.o.oN import *
from compound.o.oO import *
from database.elements.elements import db_Hal
from reaction import *
from tools.comps import simple

def r_1(comps: 'list(Compound)', is_input):
    """`oHAa -> (`oHAe_, `CH#CH`_) + `H2`"""
    react: str

    if is_input:
        oHAa = comps[0]

        n = oHAa_parse(oHAa.skeleton)

        oHAe = Compound(oHAe_create(n))
        if oHAa.skeleton.value == "CH4":
            oHAe = Compound("CH#CH")

        react = f"{oHAa} -> {oHAe} + H2"
    else:
        oHAe = Compound("CH2=CH2")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAe = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAe = comps[0]
            else:
                oHAe = comps[1]

        (n, _) = oHAe_parse(oHAe.skeleton)

        oHAa = Compound(oHAa_create(n))
        if oHAe.skeleton.value == "CH#CH":
            oHAa = Compound("CH4")

        react = f"{oHAa} -> {oHAe} + H2"

    return Reaction(react, "t c ")

def r_2(comps: 'list(Compound)', is_input):
    """`oHAa -> `oHAr + `H2`"""
    react: str

    if is_input:
        oHAa = comps[0]

        n = oHAr_parse(oHAa.skeleton) - 6
        if n < 0:
            return ""

        oHAr = oHAr_create(n)

        react = f"{oHAa} -> {oHAr} + H2"
    else:
        oHAr = Compound("BzH6")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAr = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAr = comps[0]
            else:
                oHAr = comps[1]

        n = oHAr_parse(oHAr.skeleton) + 6
        oHAa = oHAa_create(n)

        react = f"{oHAa} -> {oHAr} + H2"

    return Reaction(react, "t c: Pt")

def r_3(comps: 'list(Compound)', is_input):
    """`oHAa + `iSiNme -> `oHal + `iAcNox"""
    react: str

    if is_input:
        oHAa = Compound("CH4")
        iSiNme = Compound("Cl2")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAa = comps[0]
            else:
                iSiNme = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAa = comps[0]
                iSiNme = comps[0]
            else:
                oHAa = comps[1]
                iSiNme = comps[0]

        el = list(iSiNme.formula.consist.keys())[0].name
        if el not in db_Hal:
            return ""

        n = oHAa_parse(oHAa.skeleton)

        oHal = oHal_create(oHAa.skeleton, [(n, el)])
        iAcNox = Compound(iAc_create(el, 1))

        react = f"{oHAa} + {iSiNme} -> {oHal} + {iAcNox}"
    else:
        oHal = Compound("CCl4")
        iAcNox = Compound("HCl")
        if len(comps) == 1:
            if "oHal" in comps[0].comp_type:
                oHal = comps[0]
            else:
                iAcNox = comps[0]
        else:
            if "oHal" in comps[0].comp_type:
                oHal = comps[0]
                iAcNox = comps[0]
            else:
                oHal = comps[1]
                iAcNox = comps[0]

        (n, els) = oHal_parse(oHal.skeleton)
        (_, hals) = zip(*els)
        hals = list(set(hals))
        if len(hals) != 1:
            return ""
        hal = hals[0]

        (an, _) = iAc_oxs(iAcNox.formula)
        if an != hal:
            if len(comps) == 1:
                if "o" in comps[0].comp_type:
                    iAc = iAc_create(hal, 1)
                else:
                    iHal = Compound("C" + hal + "4")
            else:
                return ""

        oHAa = oHAa_create(n)
        iSiNme = simple(hal)

        react = f"{oHAa} + {iSiNme} -> {oHal} + {iAcNox}"

    return Reaction(react, "hv ")

def r_4(comps: 'list(Compound)', is_input):
    """`oHAa + `HNO3` -> `oNNi + `iWa`"""
    react: str

    if is_input:
        oHAa = Compound("CH4")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAa = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAa = comps[0]
            else:
                oHAa = comps[1]

        oNNi = Compound(oNNi_create(oHAa.skeleton))

        react = f"{oHAa} + HNO3 -> {oNNi} + H2O"
    else:
        oNNi = Compound("CH3(NO2)")
        if len(comps) == 1:
            if "oN" in comps[0].comp_type:
                oNNi = comps[0]
        else:
            if "oN" in comps[0].comp_type:
                oNNi = comps[0]
            else:
                oNNi = comps[1]

        n = oNNi_parse(oNNi.skeleton)[0]

        oHAa = oHAa_create(n)

        react = f"{oHAa} + HNO3 -> {oNNi} + H2O"

    return Reaction(react, "t ")

def r_5(comps: 'list(Compound)', is_input):
    """`oHAa + `O2` -> (`CO2`, `CO`, `C`) + `iWa"""
    react: str
    res = []

    if is_input:
        oHAa = Compound("CH4")
        if "oH" in comps[0].comp_type:
            oHAa = comps[0]

        res += [Reaction(f"{oHAa} + O2 -> CO2 + H2O", "t ")]
        res += [Reaction(f"{oHAa} + O2 -> CO + H2O", "t ")]
        res += [Reaction(f"{oHAa} + O2 -> C + H2O", "t ")]
    else:
        outp = []
        if len(comps) == 1:
            if comps[0].comp_type == "iWa":
                outp += [f"{comps[0]} + CO2"]
                outp += [f"{comps[0]} + CO"]
                outp += [f"{comps[0]} + C"]
            else:
                outp = [f"{comps[0]} + H2O"]
        else:
            outp = [f"{comps[0]} + {comps[1]}"]

        for o in outp:
            res += [Reaction("CH4 + O2 -> " + o, "t ")]

    return res

def r_6(comps: 'list(Compound)', is_input):
    """`oHAa + `O2` -> `oOAld + `iWa"""
    react: str

    if is_input:
        oHAa = Compound("CH4")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAa = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAa = comps[0]
            else:
                oHAa = comps[1]

        oOAld = Compound(oOAld_create(oHAa.skeleton))

        react = f"{oHAa} + O2 -> {oOAld} + H2O"
    else:
        oOAld = Compound("CH(HO)")
        if len(comps) == 1:
            if "oO" in comps[0].comp_type:
                oOAld = comps[0]
        else:
            if "oO" in comps[0].comp_type:
                oOAld = comps[0]
            else:
                oOAld = comps[1]

        n = oOAld_parse(oOAld.skeleton)

        oHAa = oHAa_create(n)

        react = f"{oHAa} + O2 -> {oOAld} + H2O"

    return Reaction(react, "t c ")
