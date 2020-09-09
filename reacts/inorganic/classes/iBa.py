from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from database.compounds.solubility import *
from element import get_oxs, get_me_oxs
from reaction import *
from tools.comps import simple
from tools.reacts import *

def r_1(comps: 'list(Compound)', is_input, nest=False, h=0, oh=0):
    """(`iBaAlk_, `iBaBa_, `iBaAm_) + (`iAcOx__, `iAcNox__, `iBaAm__, `H2O2`__) -> """\
    """(`iSaNo_, `iSaAc_, `iSaBa_, `iSaPer) + `H2O`"""
    react: str

    res = []

    if is_input:
        iBa = Compound("NaOH")
        iAc = Compound("H2SO4")
        if len(comps) == 1:
            if "iAc" in comps[0].comp_type or comps[0].formula.value == "H2O2":
                iAc = comps[0]
            else:
                iBa = comps[0]
        else:
            if "iAc" in comps[0].comp_type or comps[0].formula.value == "H2O2" or \
               "iBaAm" in comps[0].comp_type and "iAc" not in comps[1].comp_type:
                iAc = comps[0]
                iBa = comps[1]
            else:
                iAc = comps[1]
                iBa = comps[0]

        (me, me_oxs) = iBa_oxs(iBa.formula)
        iAcBa = iAc
        if iAc.comp_type == "iBaAm":
            (ame, ame_oxs) = iBa_oxs(iAc.formula)
            iAcBa = Compound(iAc_el_create(ame, ame_oxs))
        (an, an_oxs) = iAc_oxs(iAcBa.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))
        if h != 0 and oh == 0:
            iSaNo = Compound(iSaAc_create(me, me_oxs, an, an_oxs, h))
        if oh != 0 and h == 0:
            iSaNo = Compound(iSaBa_create(me, me_oxs, an, an_oxs, oh))

        if not nest and len(comps) == 1:
            if iAc.comp_type == "iBaAm":
                res += r_1([iAc, Compound("H2SO4")], True, True, h=1, oh=1)
            if iBa.comp_type == "iBaAm":
                res += r_1([iBa, Compound("NaOH")], True, True, h=1, oh=1)

        if len(comps) == 2 and iAc.formula.value != "H2O2":
            if an_oxs - h > 1 and oh == 0:
                res += r_1([iAc, iBa], True, nest=True, h=h+1, oh=0)
            if me_oxs - oh > 1 and h == 0:
                res += r_1([iAc, iBa], True, nest=True, h=0, oh=oh+1)

        react = f"{iBa} + {iAc} -> {iSaNo} + H2O"
    else:
        iSaNo = Compound("Na2SO4")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        iBa = Compound(iBa_create(me, me_oxs))
        iAc = Compound(iAc_create(an, an_oxs))

        react = f"{iBa} + {iAc} -> {iSaNo} + H2O"

    if len(res) == 0:
        return [Reaction(react)]
    else:
        res.append(Reaction(react))
        return res

def r_2(comps: 'list(Compound)', is_input):
    """(`iBaBa_, `iBaAm_, `Ca(OH)2`_, `Sr(OH)2`_, `Ba(OH)2`) ->"""\
    """(`iOxBa_, `iOxAm_, `CaO`_, `SrO`_, `BaO`_) + `H2O`"""
    react: str

    if is_input:
        iBaBa = comps[0]

        (me, me_oxs) = iBa_oxs(iBaBa.formula)
        if me == "Amm":
            return ""

        iOxBa = Compound(iOx_create(me, me_oxs))

        react = f"{iBaBa} -> {iOxBa} + H2O"
    else:
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
        if me == "NH4":
            return ""

        iBaBa = Compound(iBa_create(me, me_oxs))

        react = f"{iBaBa} -> {iOxBa} + H2O"

    return Reaction(react, "t ")

def r_3(comps: 'list(Compound)', is_input):
    """(`iBaAlk_, `iBaCo_) + (`iSaNo__, `iSaBa__, `iSaAmm__, `iSaCo__) -> """\
    """(`iBaAlk_, `iBaBa_, `iBaAm_, `iBaCo_, `AmmOH`_) + (`iSaNo__, `iSaCo__)"""
    react: str

    if is_input:
        iBaAlk = Compound("Ba(OH)2")
        iSaNo1 = Compound("ZnCl2")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
            else:
                iSaNo1 = comps[0]
                ((me, _), _) = iBa_oxs(iBaAlk.formula)
                if me == "Ba":
                    iBaAlk = Compound("NaOH")
        else:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
                iSaNo1 = comps[1]
            else:
                iBaAlk = comps[1]
                iSaNo1 = comps[0]

        (me1, me1_oxs) = iBa_oxs(iBaAlk.formula)
        ((me2, me2_oxs), (an, an_oxs)) = iSa_oxs(iSaNo1.formula)

        iBa = Compound(iBa_create(me2, me2_oxs))
        iSaNo2 = Compound(iSaNo_create(me1, me1_oxs, an, an_oxs))

        react = f"{iBaAlk} + {iSaNo1} -> {iBa} + {iSaNo2}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""
    else:
        iBa = Compound("NaOH")
        iSaNo2 = Compound("BaSO4")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type or comps[0].formula.value == "AmmOH":
                iBa = comps[0]
                if iBa.formula.value == "Ba(OH)2":
                    iSaNo2 = Compound("CaS")
            else:
                iSaNo2 = comps[0]
                (_, (an, _)) = iSa_oxs(iSaNo2.formula)
                if is_ionic_soluble(iSaNo2):
                    if "Zn" not in an:
                        iBa = Compound("Zn(OH)2")
                    else:
                        iBa = Compound("Cu(OH)2")
        else:
            if "iSi" in comps[0].comp_type:
                iBa = comps[0]
                iSaNo2 = comps[1]
            else:
                iBa = comps[1]
                iSaNo2 = comps[0]

        (me2, me2_oxs) = iBa_oxs(iBa.formula)
        ((me1, me1_oxs), (an, an_oxs)) = iSa_oxs(iSaNo2.formula)

        iBaAlk = Compound(iBa_create(me1, me1_oxs))
        if "iBaAlk" not in iBaAlk.comp_type:
            return ""
        iSaNo1 = Compound(iSaNo_create(me2, me2_oxs, an, an_oxs))

        react = f"{iBaAlk} + {iSaNo1} -> {iBa} + {iSaNo2}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""

    return Reaction(react)

def r_4(comps: 'list(Compound)', is_input):
    """`iSiMe + `iWa -> `iBaAlk + `H2`"""
    react: str

    if is_input:
        iSiMe = Compound("Na")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            else:
                iSiMe = comps[1]

        me = list(iSiMe.formula.consist.keys())[0].name
        me_oxs = get_me_oxs(me)
        if me_oxs == 0:
            return ""

        iBaAlk = Compound(iBa_create(me, me_oxs))
        if "iBaAlk" not in iBaAlk.comp_type:
            return ""

        react = f"{iSiMe} + H2O -> {iBaAlk} + H2"
    else:
        iBaAlk = Compound("NaOH")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
        else:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
            else:
                iBaAlk = comps[1]

        (me, _) = iBa_oxs(iBaAlk.formula)

        iSiMe = Compound(simple(me))

        react = f"{iSiMe} + H2O -> {iBaAlk} + H2"

    return Reaction(react)
