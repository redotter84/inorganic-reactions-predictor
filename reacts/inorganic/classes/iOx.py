from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from element import get_oxs, is_me_activer
from reaction import *
from tools.comps import simple

def r_1(comps: 'list(Compound)', is_input):
    """`iOxAlk + `iWa -> `iBaAlk"""
    react: str

    if is_input:
        iOxAlk = Compound("Na2O")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxAlk = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxAlk = comps[0]
            else:
                iOxAlk = comps[1]

        (me, me_oxs) = iOx_oxs(iOxAlk.formula)

        iBaAlk = Compound(iBa_create(me, me_oxs))

        react = f"{iOxAlk} + H2O -> {iBaAlk}"
    else:
        iBaAlk = comps[0]

        (me, me_oxs) = iBa_oxs(iBaAlk.formula)

        iOxAlk = Compound(iOx_create(me, me_oxs))

        react = f"{iOxAlk} + H2O -> {iBaAlk}"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """`iOxAc + `iWa -> `iAcOx"""
    react: str

    if is_input:
        iOxAc = Compound("SO3")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
            else:
                iOxAc = comps[1]

        if iOxAc.formula.value in ["SiO2"]:
            return ""

        (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
        if nme == "N":
            return ""

        iAcOx = Compound(iAc_el_create(nme, nme_oxs))

        react = f"{iOxAc} + H2O -> {iAcOx}"
    else:
        iAcOx = comps[0]
        if iAcOx.formula.value in ["H2SiO3"]:
            return ""

        (nme, nme_oxs) = iAc_el_oxs(iAcOx.formula)
        if nme == "N":
            return ""

        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iOxAc} + H2O -> {iAcOx}"

    return Reaction(react)

def r_3(comps: 'list(Compound)', is_input):
    """(`iOxAlk_, `iOxBa_, `iOxAm_) + (`iAcOx__, `iAcNox__, `iAcCo__) -> `iSaNo + `iWa"""
    react: str

    if is_input:
        iOxBa = Compound("CaO")
        iAc = Compound("HCl")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
            else:
                iAc = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
                iAc = comps[1]
            else:
                iOxBa = comps[1]
                iAc = comps[0]

        (me, me_oxs) = iOx_oxs(iOxBa.formula)
        (an, an_oxs) = iAc_oxs(iAc.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iOxBa} + {iAc} -> {iSaNo} + H2O"
    else:
        iSaNo = Compound("CaCl2")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)

        iOxBa = Compound(iOx_create(me, me_oxs))
        iAc = Compound(iAc_create(an, an_oxs))

        react = f"{iOxBa} + {iAc} -> {iSaNo} + H2O"

    return Reaction(react)

def r_4(comps: 'list(Compound)', is_input):
    """(`iOxAc_, `iOxAm_) + (`iBaAlk__, `iBaCo__, `Mg(OH)2`__) -> `iSaNo + `iWa"""
    react: str

    if is_input:
        iOxAc = Compound("SO3")
        iBaAlk = Compound("KOH")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
            else:
                iBaAlk = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
                iBaAlk = comps[1]
            else:
                iOxAc = comps[1]
                iBaAlk = comps[0]

        (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
        if nme == "N":
            return ""
        iAc = Compound(iAc_el_create(nme, nme_oxs))
        (me, me_oxs) = iBa_oxs(iBaAlk.formula)
        (an, an_oxs) = iAc_oxs(iAc.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iOxAc} + {iBaAlk} -> {iSaNo} + H2O"
    else:
        iSaNo = Compound("K2SO4")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        iAc = Compound(iAc_create(an, an_oxs))
        if "iAcNox" in iAc.comp_type:
            return ""
        (nme, nme_oxs) = iAc_el_oxs(iAc.formula)
        if nme == "N":
            return ""

        iBaAlk = Compound(iBa_create(me, me_oxs))
        if "iBaAlk" not in iBaAlk.comp_type:
            return ""
        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iOxAc} + {iBaAlk} -> {iSaNo} + H2O"

    return Reaction(react)

def r_5(comps: 'list(Compound)', is_input):
    """(`iOxAlk_, `iOxBa_, `iOxAm_) + (`iOxAc__, `iOxAm__) -> `iSaNo"""
    react: str

    if is_input:
        iOxBa = Compound("CaO")
        iOxAc = Compound("CO2")
        if len(comps) == 1:
            if "iOxAc" in comps[0].comp_type:
                iOxAc = comps[0]
            else:
                iOxBa = comps[0]
        else:
            if "iOxAc" in comps[0].comp_type or \
               "iOxAm" in comps[0].comp_type and "iOxAc" not in comps[0].comp_type:
                iOxAc = comps[0]
                iOxBa = comps[1]
            else:
                iOxAc = comps[1]
                iOxBa = comps[0]

        (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
        if nme == "N":
            return ""
        iAc = Compound(iAc_el_create(nme, nme_oxs))
        (me, me_oxs) = iOx_oxs(iOxBa.formula)
        (an, an_oxs) = iAc_oxs(iAc.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iOxBa} + {iOxAc} -> {iSaNo}"
    else:
        iSaNo = comps[0]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        iAcOx = Compound(iAc_create(an, an_oxs))
        if "iAcNox" in iAcOx.comp_type:
            return ""
        (nme, nme_oxs) = iAc_el_oxs(iAcOx.formula)
        if nme == "N":
            return ""

        iOxBa = Compound(iOx_create(me, me_oxs))
        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iOxBa} + {iOxAc} -> {iSaNo}"

    return Reaction(react, "t ")

def r_6(comps: 'list(Compound)', is_input):
    """(`iOxBa_, `iOxAm_) + `H2` -> `iSiMe + `iWa"""
    react: str

    if is_input:
        iOxBa = Compound("CuO")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
            else:
                iOxBa = comps[1]

        (me, me_oxs) = iOx_oxs(iOxBa.formula)
        if is_me_activer(me, me_oxs, "Al", 3) and me != "Al":
            return ""

        iSiMe = Compound(me)

        react = f"{iOxBa} + H2 -> {iSiMe} + H2O"
    else:
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
        me_oxs = get_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer(me, me_oxs, "Al", 3) and me != "Al":
            return ""

        iOxBa = Compound(iOx_create(me, me_oxs))

        react = f"{iOxBa} + H2 -> {iSiMe} + H2O"

    return Reaction(react)

def r_7(comps: 'list(Compound)', is_input):
    """(`iSiMe_, `iSiNme_) + `O2` ->"""\
    """(`iOxAlk_, `iOxBa_, `iOxAc_, `iOxAm_, `iOxNs_, `iSaPer_)"""
    react: str

    if is_input:
        iSi = Compound("P")
        if len(comps) == 1:
            if comps[0].formula.value != "O2":
                iSi = comps[0]
        else:
            if comps[0].formula.value != "O2":
                iSi = comps[0]
            else:
                iSi = comps[1]

        el = list(iSi.formula.consist.keys())[0].name
        if el in ["O", "F", "Au", "Ag", "He", "Ne", "Kr", "Xe", "Rn"]:
            return ""
        el_oxs = get_oxs(el)
        if el_oxs == 0:
            return ""

        iOx = Compound(iOx_create(el, el_oxs))
        if el == "N":
            iOx = Compound("NO")
        elif el == "Na":
            iOx = Compound("Na2O2")
        elif el in ["K", "Rb", "Cs"]:
            iOx = Compound(el + "2O2")
        elif el == "Fe":
            iOx = Compound("Fe3O4")

        react = f"{iSi} + O2 -> {iOx}"
    else:
        iOx = comps[0]

        if iOx.formula.value == "N2O5":
            return ""

        (el, _) = iOx_oxs(iOx.formula)
        if el in ["O", "F", "Au", "Ag", "He", "Ne", "Kr", "Xe", "Rn"]:
            return ""
        if el == "N" and iOx.formula.value != "NO":
            return ""

        iSi = Compound(simple(el))

        react = f"{iSi} + O2 -> {iOx}"

    return Reaction(react, "t ")

def r_8(comps: 'list(Compound)', is_input):
    """`iSiMe + `iWa -> (`iOxBa_, `iOxAm_, `iOxAc_) + `H2`"""
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
        me_oxs = get_oxs(me)
        if me_oxs == 0:
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""
        if not is_me_activer("Na", 1, me, me_oxs):
            return ""

        iOxBa = Compound(iOx_create(me, me_oxs))

        react = f"{iSiMe} + H2O -> {iOxBa} + H2"
    else:
        iOxBa = Compound("ZnO")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
            else:
                iOxBa = comps[1]

        (me, me_oxs) = iOx_oxs(iOxBa.formula)
        if is_me_activer("H", 1, me, me_oxs):
            return ""
        if not is_me_activer("Na", 1, me, me_oxs):
            return ""

        iSiMe = Compound(simple(me))
        react = f"{iSiMe} + H2O -> {iOxBa} + H2"

    return Reaction(react, "t ")
