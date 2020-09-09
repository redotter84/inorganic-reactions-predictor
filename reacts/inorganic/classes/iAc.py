from compound import *
from compound.i.iOx import *
from compound.i.iAc import *
from compound.i.iSa import *
from element import get_me_oxs, is_me_activer
from reaction import *
from tools.reacts import *

def r_1(comps: 'list(Compound)', is_input):
    """`iAcOx -> (`iOxAc_, `iOxAm_) + `H2O`"""
    react: str

    if is_input:
        iAcOx = comps[0]

        (nme, nme_oxs) = iAc_el_oxs(iAcOx.formula)
        if nme == "N":
            return ""

        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iAcOx} -> {iOxAc} + H2O"
    else:
        iOxAc = Compound("SiO2")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
            else:
                iOxAc = comps[1]

        (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
        if nme == "N":
            return ""

        iAcOx = Compound(iAc_el_create(nme, nme_oxs))

        react = f"{iAcOx} -> {iOxAc} + H2O"

    return Reaction(react, "t ")

def r_2(comps: 'list(Compound)', is_input):
    """`iSiMe + (`iAcOx_, `iAcNox_, `iAcCo_) -> `iSaNo + `H2`"""
    react: str

    if is_input:
        iAc = Compound("HCl")
        iSiMe = Compound("Zn")
        if len(comps) == 1:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
            else:
                iSiMe = comps[0]
        else:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
                iSiMe = comps[1]
            else:
                iAc = comps[1]
                iSiMe = comps[0]

        if iAc.formula.value == "HNO3":
            return ""

        me = list(iSiMe.formula.consist.keys())[0].name
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        (an, an_oxs) = iAc_oxs(iAc.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iSiMe} + {iAc} -> {iSaNo} + H2"
    else:
        iSaNo = Compound("ZnCl2")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)

        iSiMe = Compound(me)
        if is_me_activer("H", 1, me, me_oxs):
            return ""
        iAc = Compound(iAc_create(an, an_oxs))
        if iAc == Compound("HNO3"):
            return ""

        react = f"{iSiMe} + {iAc} -> {iSaNo} + H2"

    return Reaction(react)

def r_3(comps: 'list(Compound)', is_input):
    """(`iSaNo_, `iSaAc_, `iSaAmm_, `iSaAmac_, `iSaCo_) + (`iAcOx__, `iAcNox__, `iAcCo__) ->"""\
    """(`iSaNo_, `iSaAc_, `iSaAmm_, `iSaAmac_, `iSaCo_) + (`iAcOx__, `iAcNox__, `iAcCo__)"""
    react: str

    if is_input:
        iAc1 = Compound("H2SO4")
        iSaNo1 = Compound("Na2SiO3")
        if len(comps) == 1:
            if "iAc" in comps[0].comp_type:
                iAc1 = comps[0]
            else:
                iSaNo1 = comps[0]
                (_, (an, _)) = iSa_oxs(iSaNo1.formula)
                if an == "SO4":
                    iAc1 = Compound("HClO4")
        else:
            if "iAc" in comps[0].comp_type:
                iAc1 = comps[0]
                iSaNo1 = comps[1]
            else:
                iAc1 = comps[1]
                iSaNo1 = comps[0]

        ((me, me_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo1.formula)
        (an2, an2_oxs) = iAc_oxs(iAc1.formula)

        iSaNo2 = Compound(iSaNo_create(me, me_oxs, an2, an2_oxs))
        iAc2 = Compound(iAc_create(an1, an1_oxs))
        if not is_iAc_activer(iAc1.formula.value, iAc2.formula.value):
            return ""

        react = f"{iSaNo1} + {iAc1} -> {iSaNo2} + {iAc2}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""
    else:
        iAc2 = Compound("H2SiO3")
        iSaNo2 = Compound("BaSO4")
        if len(comps) == 1:
            if "iAc" in comps[0].comp_type:
                iAc2 = comps[0]
                if iAc2.formula.value == "H2SO4":
                    iSaNo2 = Compound("KClO4")
            else:
                iSaNo2 = comps[0]
        else:
            if "iAc" in comps[0].comp_type:
                iAc2 = comps[0]
                iSaNo2 = comps[1]
            else:
                iAc2 = comps[1]
                iSaNo2 = comps[0]

        ((me, me_oxs), (an2, an2_oxs)) = iSa_oxs(iSaNo2.formula)
        (an1, an1_oxs) = iAc_oxs(iAc2.formula)

        iSaNo1 = Compound(iSaNo_create(me, me_oxs, an1, an1_oxs))
        iAc1 = Compound(iAc_create(an2, an2_oxs))
        if not is_iAc_activer(iAc1.formula.value, iAc2.formula.value):
            return ""

        react = f"{iSaNo1} + {iAc1} -> {iSaNo2} + {iAc2}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""

    return Reaction(react)
