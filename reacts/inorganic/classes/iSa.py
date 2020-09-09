from compound import *
from compound.i.iOx import *
from compound.i.iAc import *
from compound.i.iSa import *
from database.compounds.gases import *
from database.compounds.solubility import *
from element import *
from reaction import *
from tools.comps import simple
from tools.reacts import *

def r_1(comps: 'list(Compound)', is_input):
    """`iSiMe + (`iSaNo_, `iSaCo_) -> `iSiMe + (`iSaNo_, `iSaCo_)"""
    react: str

    if is_input:
        iSiMe1 = Compound("Zn")
        iSaNo1 = Compound("Cu(NO3)2")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe1 = comps[0]
                me = list(iSiMe1.formula.consist.keys())[0].name
                me_oxs = get_me_oxs(me)

                if me_oxs == 0:
                    return ""
                if is_me_activer("Cu", 2, me, me_oxs):
                    return ""
            else:
                iSaNo1 = comps[0]
                ((me, me_oxs), (an, _)) = iSa_oxs(iSaNo1.formula)
                if not is_me_activer("Zn", 2, me, me_oxs) or "Zn" in an:
                    if not is_me_activer("Mg", 2, me, me_oxs):
                        return ""
                    else:
                        iSiMe1 = Compound("Mg")
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe1 = comps[0]
                iSaNo1 = comps[1]
            else:
                iSiMe1 = comps[1]
                iSaNo1 = comps[0]
        if not is_ionic_soluble(iSaNo1):
            return ""

        me1 = list(iSiMe1.formula.consist.keys())[0].name
        me1_oxs = get_me_oxs(me1)
        if me1_oxs == 0:
            return ""
        ((me2, me2_oxs), (an, an_oxs)) = iSa_oxs(iSaNo1.formula)

        if not is_me_activer(me1, me1_oxs, me2, me2_oxs):
            return ""
        if not is_me_activer("Na", 1, me1, me1_oxs):
            return ""

        iSiMe2 = Compound(simple(me2))
        iSaNo2 = Compound(iSaNo_create(me1, me1_oxs, an, an_oxs))

        react = f"{iSiMe1} + {iSaNo1} -> {iSiMe2} + {iSaNo2}"
    else:
        iSiMe2 = Compound("Cu")
        iSaNo2 = Compound("Zn(NO3)2")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe2 = comps[0]
                me = list(iSiMe2.formula.consist.keys())[0].name
                me_oxs = get_me_oxs(me)
                if me_oxs == 0:
                    return ""

                if not is_me_activer("Zn", 2, me, me_oxs):
                    if not is_me_activer("Mg", 2, me, me_oxs):
                        return ""
                    else:
                        iSaNo2 = Compound("Mg(NO3)2")
            else:
                iSaNo2 = comps[0]
                ((me, me_oxs), _) = iSa_oxs(iSaNo2.formula)
                if is_me_activer("Cu", 2, me, me_oxs):
                    return ""
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe2 = comps[0]
                iSaNo2 = comps[1]
            else:
                iSiMe2 = comps[0]
                iSaNo2 = comps[1]

        me2 = list(iSiMe2.formula.consist.keys())[0].name
        me2_oxs = get_me_oxs(me2)
        if me2_oxs == 0:
            return ""
        ((me1, me1_oxs), (an, an_oxs)) = iSa_oxs(iSaNo2.formula)

        if not is_me_activer(me1, me1_oxs, me2, me2_oxs):
            return ""
        if not is_me_activer("Na", 1, me1, me1_oxs):
            return ""

        iSiMe1 = Compound(simple(me1))
        iSaNo1 = Compound(iSaNo_create(me2, me2_oxs, an, an_oxs))

        if not is_ionic_soluble(iSaNo1):
            return ""

        react = f"{iSiMe1} + {iSaNo1} -> {iSiMe2} + {iSaNo2}"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """(`iSaNo_, `iSaAmm_, `iSaCo_) + (`iSaNo__, `iSaAmm__, `iSaCo__) -> """\
    """(`iSaNo_, `iSaAmm_, `iSaCo_) + (`iSaNo__, `iSaAmm__, `iSaCo__)"""
    react: str

    if is_input:
        iSaNo1 = Compound("Na2SO4")
        iSaNo2 = Compound("BaCl2")
        if len(comps) == 1:
            iSaNo1 = comps[0]
            ((me, _), (an, an_oxs)) = iSa_oxs(iSaNo1.formula)
            if me == "Ba" and an != "SO4":
                iSaNo2 = Compound("Na2SO4")
            elif an not in ["F", "SO4", "NO3"]:
                iSaNo2 = Compound("AgNO3")
            else:
                if an == "SO4":
                    iSaNo2 = Compound("BaCl2")
                elif an == "F":
                    iSaNo2 = Compound("MgCl2")
                elif an == "NO3":
                    iSaNo2 = Compound("SnCl2")
        else:
            iSaNo1 = comps[0]
            iSaNo2 = comps[1]

        ((me1, me1_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo1.formula)
        ((me2, me2_oxs), (an2, an2_oxs)) = iSa_oxs(iSaNo2.formula)

        if not is_ionic_soluble(iSaNo1) or not is_ionic_soluble(iSaNo2):
            return ""

        iSaNo3 = Compound(iSaNo_create(me2, me2_oxs, an1, an1_oxs))
        iSaNo4 = Compound(iSaNo_create(me1, me1_oxs, an2, an2_oxs))

        react = f"{iSaNo1} + {iSaNo2} -> {iSaNo3} + {iSaNo4}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""
    else:
        iSaNo3 = Compound("NaCl")
        iSaNo4 = Compound("BaSO4")
        if len(comps) == 1:
            iSaNo3 = comps[0]
            ((me, _), (an, _)) = iSa_oxs(iSaNo3.formula)
            if an == "SO4":
                if me != "Ba":
                    iSaNo4 = Compound("CaCO3")
                else:
                    iSaNo4 = Compound("NaCl")
        else:
            iSaNo3 = comps[0]
            iSaNo4 = comps[1]

        ((me1, me1_oxs), (an2, an2_oxs)) = iSa_oxs(iSaNo3.formula)
        ((me2, me2_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo4.formula)

        iSaNo1 = Compound(iSaNo_create(me2, me2_oxs, an2, an2_oxs))
        iSaNo2 = Compound(iSaNo_create(me1, me1_oxs, an1, an1_oxs))

        if not is_ionic_soluble(iSaNo1) or not is_ionic_soluble(iSaNo2):
            return ""

        react = f"{iSaNo1} + {iSaNo2} -> {iSaNo3} + {iSaNo4}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""

    return Reaction(react)

def r_3(comps: 'list(Compound)', is_input):
    """`iSaNo -> (`iOxBa_, `iOxAm_) + (`iOxAc__, `iOxAm__)"""
    react: str

    if is_input:
        iSaNo = comps[0]

        if Element("O") not in iSaNo.formula.consist:
            return ""

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if Element(me).elem_sub_type == "AlkMe":
            return ""

        iAc = Compound(iAc_create(an, an_oxs))
        (nme, nme_oxs) = iAc_el_oxs(iAc.formula)
        if nme == "N":
            return ""

        iOxBa = Compound(iOx_create(me, me_oxs))
        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iSaNo} -> {iOxBa} + {iOxAc}"
    else:
        iOxBa = Compound("CaO")
        iOxAc = Compound("CO2")
        if len(comps) == 1:
            if "iOxAc" in comps[0].comp_type:
                iOxAc = comps[0]
            else:
                iOxBa = comps[0]
        else:
            if "iOxAc" in comps[0].comp_type or \
               "iOxAm" in comps[0].comp_type and "iOxAc" not in comps[1].comp_type:
                iOxAc = comps[0]
                iOxBa = comps[1]
            else:
                iOxAc = comps[1]
                iOxBa = comps[0]

        (me, me_oxs) = iOx_oxs(iOxBa.formula)
        if Element(me).elem_sub_type == "AlkMe":
            return ""

        (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
        if nme == "N":
            return ""
        iAc = Compound(iAc_el_create(nme, nme_oxs))
        (an, an_oxs) = iAc_oxs(iAc.formula)

        if an == "NO3":
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))

        react = f"{iSaNo} -> {iOxBa} + {iOxAc}"

    return Reaction(react, "t ")

def r_4(comps: 'list(Compound)', is_input):
    """`iSaNo + `iOxAc -> `iSaNo + `iOxAc"""
    react: str

    if is_input:
        iSaNo1 = Compound("Na2CO3")
        iOxAc1 = Compound("SO3")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxAc1 = comps[0]
            else:
                iSaNo1 = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxAc1 = comps[0]
                iSaNo1 = comps[1]
            else:
                iOxAc1 = comps[1]
                iSaNo1 = comps[0]

        ((me, me_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo1.formula)
        iAc1 = Compound(iAc_create(an1, an1_oxs))
        if iAc1.comp_type == "iAcNox":
            return ""
        (nme1, nme1_oxs) = iAc_el_oxs(iAc1.formula)
        if nme1 == "N":
            return ""

        (nme2, nme2_oxs) = iOx_oxs(iOxAc1.formula)
        if nme2 == "N":
            return ""
        iAc2 = Compound(iAc_el_create(nme2, nme2_oxs))
        if iAc2.comp_type == "iAcNox":
            return ""
        (an2, an2_oxs) = iAc_oxs(iAc2.formula)

        if is_gase(iOxAc1):
            return ""

        iOxAc2 = Compound(iOx_create(nme1, nme1_oxs))
        iSaNo2 = Compound(iSaNo_create(me, me_oxs, an2, an2_oxs))

        react = f"{iSaNo1} + {iOxAc1} -> {iSaNo2} + {iOxAc2}"

        xg = Reaction(react)

        if find_if(xg.outp, lambda c: is_gase(c)) == -1:
            return ""
    else:
        iSaNo2 = Compound("Na2SO4")
        iOxAc2 = Compound("CO2")
        if len(comps) == 1:
            if "iOx" in comps[0].comp_type:
                iOxAc2 = comps[0]
            else:
                iSaNo2 = comps[0]
        else:
            if "iOx" in comps[0].comp_type:
                iOxAc2 = comps[0]
                iSaNo2 = comps[1]
            else:
                iOxAc2 = comps[1]
                iSaNo2 = comps[0]

        ((me, me_oxs), (an2, an2_oxs)) = iSa_oxs(iSaNo2.formula)
        iAc2 = Compound(iAc_create(an2, an2_oxs))
        if iAc2.comp_type == "iAcNox":
            return ""
        (nme2, nme2_oxs) = iAc_el_oxs(iAc2.formula)
        if nme2 == "N":
            return ""

        (nme1, nme1_oxs) = iOx_oxs(iOxAc2.formula)
        if nme1 == "N":
            return ""
        iAc1 = Compound(iAc_el_create(nme1, nme1_oxs))
        if iAc1.comp_type == "iAcNox":
            return ""
        (an1, an1_oxs) = iAc_oxs(iAc1.formula)

        iSaNo1 = Compound(iSaNo_create(me, me_oxs, an1, an1_oxs))
        iOxAc1 = Compound(iOx_create(nme2, nme2_oxs))

        if is_gase(iOxAc1):
            return ""

        react = f"{iSaNo1} + {iOxAc1} -> {iSaNo2} + {iOxAc2}"

        xg = Reaction(react)

        if find_if(xg.outp, lambda c: is_gase(c)) == -1:
            return ""

    return Reaction(react, "t ")
