from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from database.compounds.solubility import *
from element import get_me_oxs, is_me_activer
from reaction import *
from tools.comps import simple
from tools.reacts import *

def r_1(comps: 'list(Compound)', is_input):
    """`iSaAc + (`iBaAlk_, `iBaBa_, `iBaAm_) -> `iSaNo + `iWa"""
    react: str

    if is_input:
        iSaAc = Compound("NaHCO3")
        iBa = Compound("NaOH")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaAc = comps[0]
                ((me, me_oxs), _) = iSa_oxs(iSaAc.formula)
                iBa = Compound(iBa_create(me, me_oxs))
            else:
                iBa = comps[0]
                (me, me_oxs) = iBa_oxs(iBa.formula)
                iSaAc = Compound(iSaAc_create(me, me_oxs, "CO3", 2))
        else:
            if "iSa" in comps[0].comp_type:
                iSaAc = comps[0]
                iBa = comps[1]
            else:
                iSaAc = comps[1]
                iBa = comps[0]

        ((me1, me1_oxs), (an, an_oxs)) = iSa_oxs(iSaAc.formula)
        (me2, me2_oxs) = iBa_oxs(iBa.formula)
        if (me1, me1_oxs) != (me2, me2_oxs):
            return ""

        iSaNo = Compound(iSaNo_create(me1, me1_oxs, an, an_oxs))

        react = f"{iSaAc} + {iBa} -> {iSaNo} + H2O"
    else:
        iSaNo = Compound("Na2CO3")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an_oxs == 1:
            return ""

        iSaAc = Compound(iSaAc_create(me, me_oxs, an, an_oxs))
        iBa = Compound(iBa_create(me, me_oxs))

        react = f"{iSaAc} + {iBa} -> {iSaNo} + H2O"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """"(`iSaAc_, `iSaAmac_) + (`iSaNo__, `iSaAmm__) -> """\
    """"(`iSaNo_, `iSaAmm_) + (`iSaNo__, `iSaAmm__) + (`iAcNox, `iAcOx)"""
    react: str

    if is_input:
        iSaAc = Compound("NaHSO4")
        iSaNo1 = Compound("BaCl2")
        if len(comps) == 1:
            if "iSaAc" in comps[0].comp_type:
                iSaAc = comps[0]
                (_, (an, _)) = iSa_oxs(iSaAc.formula)
                if an != "SO4":
                    iSaNo1 = Compound("AgNO3")
                else:
                    if an == "SO4":
                        iSaNo1 = Compound("BaCl2")
            else:
                iSaNo1 = comps[0]
                ((me, _), (an, _)) = iSa_oxs(iSaNo1.formula)
                if me != "Ba":
                    if an != "S":
                        iSaAc = Compound("Ba(HS)2")
                    else:
                        iSaAc = Compound("Ba(HCO3)2")
                else:
                    if an != "S":
                        iSaAc = Compound("Ca(HS)2")
                    else:
                        iSaAc = Compound("Ca(HCO3)2")
        else:
            if "iSaAc" in comps[0].comp_type:
                iSaAc = comps[0]
                iSaNo1 = comps[1]
            else:
                iSaAc = comps[1]
                iSaNo1 = comps[0]

        ((me1, me1_oxs), (an1, an1_oxs)) = iSa_oxs(iSaAc.formula)
        ((me2, me2_oxs), (an2, an2_oxs)) = iSa_oxs(iSaNo1.formula)

        if not is_ionic_soluble(iSaNo1):
            return ""

        iSaNo2 = Compound(iSaNo_create(me2, me2_oxs, an1, an1_oxs))
        iSaNo3 = Compound(iSaNo_create(me1, me1_oxs, an2, an2_oxs))
        iAc = Compound(iAc_create(an1, an1_oxs))

        react = f"{iSaAc} + {iSaNo1} -> {iSaNo2} + {iSaNo3} + {iAc}"
        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""
    else:
        iSaNo2 = Compound("Na2CO3")
        iSaNo3 = Compound("BaSO4")
        iAc = Compound("H2SO4")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo2 = comps[0]
                ((me, _), (an, _)) = iSa_oxs(iSaNo2.formula)
                if me == "Ba":
                    if an == "SO4":
                        iSaNo3 = Compound("Na2S")
                    else:
                        iSaNo3 = Compound("MgSO4")
                else:
                    if an == "SO4":
                        iSaNo3 = Compound("BaCO3")
                    else:
                        iSaNo3 = Compound("BaSO4")
            else:
                iAc = comps[0]
                (an, an_oxs) = iAc_oxs(iAc.formula)
                iSaNo2 = Compound(iSaNo_create("Na", 1, an, an_oxs))
                if an == "SO4":
                    iSaNo3 = Compound("MgCO3")
        elif len(comps) == 2:
            if "iAc" in comps[0].comp_type or "iAc" in comps[1].comp_type:
                for i in range(0, 2):
                    if "iAc" in comps[i].comp_type:
                        iAc = comps[i]
                        iSaNo2 = comps[i-1]
                        (an1, an1_oxs) = iAc_oxs(iAc.formula)
                        ((me, _), (an2, an2_oxs)) = iSa_oxs(iSaNo2.formula)
                        if an1 == an2:
                            if an1 == "SO4":
                                iSaNo3 = Compound("Na2CO3")
                            break;
                        else:
                            if an1 != "S":
                                if me != "Ba":
                                    iSaNo3 = Compound(iSaNo_create("Ba", 2,
                                      an1, an1_oxs))
                                else:
                                    iSaNo3 = Compound("Na2SO3")
                            else:
                                iSaNo3 = Compound("CaS")
            else:
                iSaNo2 = comps[0]
                iSaNo3 = comps[1]
                (_, (an1, an1_oxs)) = iSa_oxs(iSaNo2.formula)
                if an1_oxs == 1:
                    (_, (an2, an2_oxs)) = iSa_oxs(iSaNo3.formula)
                    iAc = Compound(iAc_create(an2, an2_oxs))
                iAc = Compound(iAc_create(an1, an1_oxs))
        else:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
                iSaNo2 = comps[1]
                iSaNo3 = comps[2]
            elif "iAc" in comps[1].comp_type:
                iAc = comps[1]
                iSaNo2 = comps[0]
                iSaNo3 = comps[2]
            else:
                iAc = comps[2]
                iSaNo2 = comps[0]
                iSaNo3 = comps[1]

        ((me1, me1_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo2.formula)
        ((me2, me2_oxs), (an2, an2_oxs)) = iSa_oxs(iSaNo3.formula)
        (an3, an3_oxs) = iAc_oxs(iAc.formula)

        if an3_oxs == 1:
            return ""
        if me1 == me2 or an1 == an2:
            return ""

        iSaAc: Compound
        iSaNo1: Compound
        if an1 == an3:
            iSaAc = Compound(iSaAc_create(me2, me2_oxs, an1, an1_oxs))
            iSaNo1 = Compound(iSaNo_create(me1, me1_oxs, an2, an2_oxs))
        elif an2 == an3:
            iSaAc = Compound(iSaAc_create(me1, me1_oxs, an2, an2_oxs))
            iSaNo1 = Compound(iSaNo_create(me2, me2_oxs, an1, an1_oxs))
        else:
            return ""

        if not is_ionic_soluble(iSaNo1):
            return ""

        react = f"{iSaAc} + {iSaNo1} -> {iSaNo2} + {iSaNo3} + {iAc}"

        xg = Reaction(react)

        if not is_exchange(xg.outp):
            return ""

    return Reaction(react)

def r_3(comps: 'list(Compound)', is_input):
    """iSaAc -> `iSaNo + `iOxAc + `iWa"""
    react: str

    if is_input:
        iSaAc = Compound("NaHSO4")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaAc = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaAc = comps[0]
            else:
                iSaAc = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaAc.formula)
        iAc = Compound(iAc_create(an, an_oxs))
        if "iAcNox" in iAc.comp_type:
            return ""
        (nme, nme_oxs) = iAc_el_oxs(iAc.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))
        iOxAc = Compound(iOx_create(nme, nme_oxs))

        react = f"{iSaAc} -> {iSaNo} + {iOxAc} + H2O"
    else:
        iSaNo = Compound("Na2SO4")
        iOxAc = Compound("SO3")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                (_, (an, an_oxs)) = iSa_oxs(iSaNo.formula)
                iAc = Compound(iAc_create(an, an_oxs))
                (nme, nme_oxs) = iAc_el_oxs(iAc.formula)
                iAcOx = Compound(iOx_create(nme, nme_oxs))
            elif "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
                (nme, nme_oxs) = iOx_oxs(iOxAc.formula)
                iAc = Compound(iAc_el_create(nme, nme_oxs))
                (an, an_oxs) = iAc_oxs(iAc.formula)
                iSaNo = Compound(iSaNo_create("Na", 1, an, an_oxs))
        elif len(comps) == 2:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSa" in comps[1].comp_type:
                iSaNo = comps[1]
            if "iOx" in comps[0].comp_type:
                iOxAc = comps[0]
            elif "iOx" in comps[1].comp_type:
                iOxAc = comps[1]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxAc = comps[1]
                else:
                    iOxAc = comps[2]
            elif "iSa" in comps[1].comp_type:
                iSaNo = comps[1]
                if "iOx" in comps[0].comp_type:
                    iOxAc = comps[0]
                else:
                    iOxAc = comps[1]
            else:
                iSaNo = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxAc = comps[1]
                else:
                    iOxAc = comps[2]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if an_oxs == 1:
            return ""
        iAc = Compound(iAc_create(an, an_oxs))
        if "iAcNox" in iAc.comp_type:
            return ""

        (nme1, nme1_oxs) = iAc_el_oxs(iAc.formula)
        (nme2, nme2_oxs) = iOx_oxs(iOxAc.formula)

        if (nme1, nme1_oxs) != (nme2, nme2_oxs):
            return ""

        iSaAc = Compound(iSaAc_create(me, me_oxs, an, an_oxs))

        react = f"{iSaAc} -> {iSaNo} + {iOxAc} + H2O"

    return Reaction(react, "t ")

def r_4(comps: 'list(Compound)', is_input):
    """`iSiMe + `iSaAc -> `iSiMe + `iSaNo + (`iAcOx_, `iAcNox_)"""
    react: str

    if is_input:
        iSiMe1 = Compound("Mg")
        iSaAc = Compound("Cu(HSO4)2")
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
                iSaAc = comps[0]
                ((me, me_oxs), _) = iSa_oxs(iSaAc.formula)
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe1 = comps[0]
                iSaAc = comps[1]
            else:
                iSiMe1 = comps[1]
                iSaAc = comps[0]

        me1 = list(iSiMe1.formula.consist.keys())[0].name
        me1_oxs = get_me_oxs(me1)
        if me1_oxs == 0:
            return ""
        ((me2, me2_oxs), (an, an_oxs)) = iSa_oxs(iSaAc.formula)
        if not is_me_activer(me1, me1_oxs, me2, me2_oxs):
            return ""
        if not is_me_activer("Na", 1, me1, me1_oxs):
            return ""

        iSiMe2 = Compound(simple(me2))
        iSaNo = Compound(iSaNo_create(me1, me1_oxs, an, an_oxs))
        iAc = Compound(iAc_create(an, an_oxs))

        react = f"{iSiMe1} + {iSaAc} -> {iSiMe2} + {iSaNo} + {iAc}"
    else:
        iSiMe2 = Compound("Cu")
        iSaNo = Compound("MgSO4")
        iAc = Compound("H2SO4")
        if len(comps) == 1:
            if "iSi" in comps[0].comp_type:
                iSiMe2 = comps[0]
                me = list(iSiMe2.formula.consist.keys())[0].name
                me_oxs = get_me_oxs(me)
                if me_oxs == 0:
                    return ""
            elif "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
                iAc = Compound(iAc_create(an, an_oxs))
                if is_me_activer("Cu", 2, me, me_oxs):
                    return ""
                if me == "Cu":
                    iSiMe = Compound("Ag")
            else:
                iAc = comps[0]
                (an, an_oxs) = iAc_oxs(iAc.formula)
                iSaNo = Compound(iSaNo_create("Zn", 2, an, an_oxs))
        elif len(comps) == 2:
            for i in range(0, 2):
                for j in range(0, 2):
                    if "iSi" in comps[i].comp_type and "iSa" in comps[j].comp_type:
                        iSiMe = comps[i]
                        iSaNo = comps[j]
                        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
                        iAc = Compound(iAc_create(an, an_oxs))
                        break
                    if "iSi" in comps[i].comp_type and "iAc" in comps[j].comp_type:
                        iSiMe = comps[i]
                        iAc = comps[j]
                        (an, an_oxs) = iAc_oxs(iAc.formula)
                        iSaNo = Compound(iSaNo_create("Mg", 2, an, an_oxs))
                        break
                    if "iSa" in comps[i].comp_type and "iAc" in comps[j].comp_type:
                        iSaNo = comps[i]
                        iAc = comps[j]
                        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
                        if me == "Cu":
                            iSiMe = Compound("Ag")
                        break
        else:
            if "iSi" in comps[0].comp_type:
                iSiMe2 = comps[0]
                if "iSa" in comps[1].comp_type:
                    iSaNo = comps[1]
                    iAc = comps[2]
                else:
                    iSaNo = comps[2]
                    iAc = comps[1]
            elif "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                if "iSi" in comps[1].comp_type:
                    iSiMe2 = comps[1]
                    iAc = comps[2]
                else:
                    iSiMe2 = comps[2]
                    iAc = comps[1]
            elif "iAc" in comps[0].comp_type:
                iAc = comps[0]
                if "iSi" in comps[1].comp_type:
                    iSiMe2 = comps[1]
                    iSaNo = comps[2]
                else:
                    iSiMe2 = comps[2]
                    iSaNo = comps[1]

        me2 = list(iSiMe2.formula.consist.keys())[0].name
        me2_oxs = get_me_oxs(me2)
        if me2_oxs == 0:
            return ""
        ((me1, me1_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo.formula)
        (an2, an2_oxs) = iAc_oxs(iAc.formula)
        if an1 != an2:
            return ""
        if an1_oxs == 1:
            return ""
        if not is_me_activer(me1, me1_oxs, me2, me2_oxs):
            return ""
        if not is_me_activer("Na", 1, me1, me1_oxs):
            return ""

        iSiMe1 = Compound(simple(me1))
        iSaAc = Compound(iSaAc_create(me2, me2_oxs, an1, an1_oxs))

        react = f"{iSiMe1} + {iSaAc} -> {iSiMe2} + {iSaNo} + {iAc}"

    return Reaction(react)

def r_5(comps: 'list(Compound)', is_input):
    """(`iSaNo_, `iSaAmm_) + (`iAcOx__, `iAcNox__) -> (`iSaAc_, `iSaAmac_)"""
    react: str

    if is_input:
        iSaNo = Compound("K2SO4")
        iAc = Compound("H2SO4")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                (_, (an, an_oxs)) = iSa_oxs(iSaNo.formula)
                iAc = Compound(iAc_create(an, an_oxs))
            else:
                iAc = comps[0]
                (an, an_oxs) = iAc_oxs(iAc.formula)
                iSaNo = Compound(iSaNo_create("K", 1, an, an_oxs))
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                iAc = comps[1]
            else:
                iSaNo = comps[1]
                iAc = comps[0]

        ((me, me_oxs), (an1, an1_oxs)) = iSa_oxs(iSaNo.formula)
        (an2, an2_oxs) = iAc_oxs(iAc.formula)
        if an1 != an2:
            return ""
        if an1_oxs == 1:
            return ""

        iSaAc = Compound(iSaAc_create(me, me_oxs, an1, an1_oxs))

        react = f"{iSaNo} + {iAc} -> {iSaAc}"
    else:
        iSaAc = comps[0]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaAc.formula)
        if an_oxs == 1:
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))
        iAc = Compound(iAc_create(an, an_oxs))

        react = f"{iSaNo} + {iAc} -> {iSaAc}"

    return Reaction(react)
