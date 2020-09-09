from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from element import get_me_oxs, get_nme_oxs, is_me_activer
from reaction import *
from tools.comps import simple

def r_1(comps: 'list(Compound)', is_input):
    """`iBaAlk -> `iSiMe + `O2` + `iWa"""
    react: str

    if is_input:
        iBaAlk = comps[0]

        (me, me_oxs) = iBa_oxs(iBaAlk.formula)

        iSiMe = Compound(simple(me))

        react = f"{iBaAlk} -> {iSiMe} + O2 + H2O"
    else:
        iSiMe = Compound("Na")
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
        me_oxs: int
        if Element(me).elem_sub_type == "AlkMe":
            me_oxs = 1
        elif Element(me).elem_sub_type == "AlkEMe":
            me_oxs = 2
        else:
            return ""

        iBaAlk = Compound(iBa_create(me, me_oxs))

        react = f"{iBaAlk} -> {iSiMe} + O2 + H2O"

    return Reaction(react, "te- ")

def r_2(comps: 'list(Compound)', is_input):
    """`iAcNox -> `iSiNme + `H2`"""
    react: str

    if is_input:
        iAcNox = comps[0]

        (nme, _) = iAc_el_oxs(iAcNox.formula)

        iSiNme = Compound(simple(nme))

        react = f"{iAcNox} -> H2 + {iSiNme}"
    else:
        iSiNme = Compound("Cl2")
        if len(comps) == 1:
            if comps[0].formula.value != "H2":
                iSiNme = comps[0]
        else:
            if comps[0].formula.value != "H2":
                iSiNme = comps[0]
            else:
                iSiNme = comps[1]
        nme = list(iSiNme.formula.consist.keys())[0].name
        if nme in ["O", "H"]:
            return ""
        nme_oxs = get_nme_oxs(nme)
        if nme_oxs == 0:
            return ""

        iAcNox = Compound(iAc_create(nme, nme_oxs))
        if "iAc" not in iAcNox.comp_type:
            return ""

        react = f"{iAcNox} -> H2 + {iSiNme}"

    return Reaction(react, "e- ")

def r_3(comps: 'list(Compound)', is_input):
    """`iSaNo -> `iSiMe + `iSiNme"""
    react: str

    me: str; me_oxs: int
    if is_input:
        iSaNo = comps[0]

        if len(iSaNo.formula.consist) > 2:
            return ""

        ((me, me_oxs), (nme, _)) = iSa_oxs(iSaNo.formula)

        iSiMe = Compound(simple(me))
        iSiNme = Compound(simple(nme))

        react = f"{iSaNo} -> {iSiMe} + {iSiNme}"
    else:
        iSiMe = Compound("Na")
        iSiNme = Compound("Cl2")
        if len(comps) == 1:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiNme = comps[0]
        else:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
                iSiNme = comps[1]
            else:
                iSiMe = comps[1]
                iSiNme = comps[0]

        me = list(iSiMe.formula.consist.keys())[0].name
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""

        nme = list(iSiNme.formula.consist.keys())[0].name
        if nme in ["O", "H"]:
            return ""
        nme_oxs = get_nme_oxs(nme)
        if nme_oxs == 0:
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, nme, nme_oxs))
        if "iSa" not in iSaNo.comp_type:
            return ""

        react = f"{iSaNo} -> {iSiMe} + {iSiNme}"

    if not is_me_activer("Al", 3, me, me_oxs) or me == "Al":
        return Reaction(react, "te- ")
    else:
        return Reaction(react, "e- ")

def r_4(comps: 'list(Compound)', is_input):
    """`iSaNo -> `iSiMe + `iOxAc + `O2`"""
    react: str

    if is_input:
        iSaNo = comps[0]

        ((me, _), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        iAc = Compound(iAc_create(an, an_oxs))
        if "iAcNox" in iAc.comp_type:
            return ""

        (nme, nme_oxs) = iAc_el_oxs(iAc.formula)
        if nme == "N":
            return ""

        iSiMe = Compound(simple(me))
        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iSaNo} -> {iSiMe} + {iOxAc} + O2"
    else:
        iSiMe = Compound("Na")
        iOxAc = Compound("SO3")
        if len(comps) == 1:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
            elif "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
        elif len(comps) == 2:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxAc = comps[1]
            elif "iSiMe" in comps[1].comp_type:
                iSiMe = comps[1]
                if "iOx" in comps[0].comp_type:
                    iOxAc = comps[0]
            else:
                if "iOx" in comps[0].comp_type:
                    iOxAc = comps[0]
                elif "iOx" in comps[1].comp_type:
                    iOxAc = comps[1]
        else:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxAc = comps[1]
                else:
                    iOxAc = comps[2]
            elif "iSiMe" in comps[1].comp_type:
                iSiMe = comps[1]
                if "iOx" in comps[0].comp_type:
                    iOxAc = comps[0]
                else:
                    iOxAc = comps[2]
            else:
                iSiMe = comps[2]
                if "iOx" in comps[0].comp_type:
                    iOxAc = comps[0]
                else:
                    iOxAc = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""

        (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
        if nme == "N":
            return ""
        iAcOx = Compound(iAc_el_create(nme, nme_oxs))
        (an, an_oxs) = iAc_oxs(iAcOx.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iSaNo} -> {iSiMe} + {iOxAc} + O2"

    return Reaction(react, "te- ")

def r_5(comps: 'list(Compound)', is_input):
    """`iSaNo + `iWa -> (`iBaAlk_, `iBaBa_, `iBaAm_) + `iSiNme + `H2`"""
    react: str

    if is_input:
        iSaNo = Compound("NaCl")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if is_me_activer("Al", 3, me, me_oxs):
            return ""

        iAc = Compound(iAc_create(an, an_oxs))
        if "iAcOx" in iAc.comp_type:
            return ""
        (nme, _) = iAc_el_oxs(iAc.formula)

        iBa = Compound(iBa_create(me, me_oxs))
        iSiNme = Compound(simple(nme))

        react = f"{iSaNo} + H2O -> {iBa} + {iSiNme} + H2"
    else:
        iBa = Compound("NaOH")
        iSiNme = Compound("Cl2")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type:
                iBa = comps[0]
            elif comps[0].formula.value != "H2":
                iSiNme = comps[0]
        elif len(comps) == 2:
            if "iBa" in comps[0].comp_type:
                iBa = comps[0]
                if comps[1].formula.value != "H2":
                    iSiNme = comps[1]
            elif "iBa" in comps[1].comp_type:
                iBa = comps[1]
                if comps[0].formula.value != "H2":
                    iSiNme = comps[0]
            else:
                if comps[0].formula.value != "H2":
                    iSiNme = comps[0]
                else:
                    iSiNme = comps[1]
        else:
            if "iBa" in comps[0].comp_type:
                iBa = comps[0]
                if comps[1].formula.value != "H2":
                    iSiNme = comps[1]
                else:
                    iSiNme = comps[2]
            if "iBa" in comps[1].comp_type:
                iBa = comps[1]
                if comps[0].formula.value != "H2":
                    iSiNme = comps[0]
                else:
                    iSiNme = comps[2]
            if "iBa" in comps[2].comp_type:
                iBa = comps[2]
                if comps[0].formula.value != "H2":
                    iSiNme = comps[0]
                else:
                    iSiNme = comps[1]

        (me, me_oxs) = iBa_oxs(iBa.formula)
        if me == "Amm":
            return ""
        if is_me_activer("Al", 3, me, me_oxs):
            return ""

        nme = list(iSiNme.formula.consist.keys())[0].name
        if nme in ["O", "H"]:
            return ""
        nme_oxs = get_nme_oxs(nme)
        if nme_oxs == 0:
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, nme, nme_oxs))
        if "iSa" not in iSaNo.comp_type:
            return ""

        react = f"{iSaNo} + H2O -> {iBa} + {iSiNme} + H2"

    return Reaction(react, "e- ")

def r_6(comps: 'list(Compound)', is_input):
    """`iSaNo + `iWa -> `iSiMe + `iAcOx + `O2`"""
    react: str

    if is_input:
        iSaNo = Compound("ZnSO4")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if not is_me_activer("Al", 3, me, me_oxs) or me == "Al":
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""

        iSiMe = Compound(simple(me))
        iAcOx = Compound(iAc_create(an, an_oxs))
        if "iAcNox" in iAcOx.comp_type:
            return ""

        react = f"{iSaNo} + H2O -> {iSiMe} + {iAcOx} + O2"
    else:
        iSiMe = Compound("Zn")
        iAcOx = Compound("H2SO4")
        if len(comps) == 1:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
            elif "iAc" in comps[0].comp_type:
                iAcOx = comps[0]
        elif len(comps) == 2:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
                if "iAc" in comps[0].comp_type:
                    iAcOx = comps[1]
            elif "iSiMe" in comps[1].comp_type:
                iSiMe = comps[1]
                if "iAc" in comps[0].comp_type:
                    iAcOx = comps[0]
            else:
                if "iAc" in comps[0].comp_type:
                    iAcOx = comps[0]
                else:
                    iAcOx = comps[1]
        else:
            if "iSiMe" in comps[0].comp_type:
                iSiMe = comps[0]
                if "iAc" in comps[0].comp_type:
                    iAcOx = comps[1]
                else:
                    iAcOx = comps[2]
            if "iSiMe" in comps[1].comp_type:
                iSiMe = comps[1]
                if "iAc" in comps[0].comp_type:
                    iAcOx = comps[0]
                else:
                    iAcOx = comps[2]
            if "iSiMe" in comps[2].comp_type:
                iSiMe = comps[2]
                if "iAc" in comps[0].comp_type:
                    iAcOx = comps[0]
                else:
                    iAcOx = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""

        if not is_me_activer("Al", 3, me, me_oxs) or me == "Al":
            return ""
        if is_me_activer("H", 1, me, me_oxs):
            return ""
        (an, an_oxs) = iAc_oxs(iAcOx.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iSaNo} + H2O -> {iSiMe} + {iAcOx} + O2"

    return Reaction(react, "e- ")
