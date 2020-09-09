from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from reaction import *

def r_1(comps: 'list(Compound)', is_input):
    """`iSaBa + (`iAcOx_, `iAcNox_) -> `iSaNo + `iWa"""
    react: str

    if is_input:
        iSaBa = Compound("Cu(OH)Cl")
        iAc = Compound("HCl")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaBa = comps[0]
                (_, (an, an_oxs)) = iSa_oxs(iSaBa.formula)
                iAc = Compound(iAc_create(an, an_oxs))
            else:
                iAc = comps[0]
                (an, an_oxs) = iAc_oxs(iAc.formula)
                iSaBa = Compound(iSaBa_create("Cu", 2, an, an_oxs))
        else:
            if "iSa" in comps[0].comp_type:
                iSaBa = comps[0]
                iAc = comps[1]
            else:
                iSaBa = comps[1]
                iAc = comps[0]

        ((me, me_oxs), (an1, an1_oxs)) = iSa_oxs(iSaBa.formula)
        (an2, an2_oxs) = iAc_oxs(iAc.formula)
        if (an1, an1_oxs) != (an2, an2_oxs):
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, an1, an1_oxs))

        react = f"{iSaBa} + {iAc} -> {iSaNo} + H2O"
    else:
        iSaNo = Compound("CuCl2")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            else:
                iSaNo = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if me_oxs == 1:
            return ""

        iSaBa = Compound(iSaBa_create(me, me_oxs, an, an_oxs))
        iAc = Compound(iAc_create(an, an_oxs))

        react = f"{iSaBa} + {iAc} -> {iSaNo} + H2O"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """`iSaBa -> `iSaNo + (`iOxAlk, `iOxBa, `iOxAm) + `iWa"""
    react: str

    if is_input:
        iSaBa = Compound("Cu(OH)Cl")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaBa = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaBa = comps[0]
            else:
                iSaBa = comps[1]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaBa.formula)

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))
        iOxBa = Compound(iOx_create(me, me_oxs))

        react = f"{iSaBa} -> {iSaNo} + {iOxBa} + H2O"
    else:
        iSaNo = Compound("CuCl2")
        iOxBa = Compound("CuO")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                ((me, me_oxs), _) = iSa_oxs(iSaNo.formula)
                iOxBa = Compound(iOx_create(me, me_oxs))
            elif "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
                (me, me_oxs) = iOx_oxs(iOxBa.formula)
                iSaNo = Compound(iSaNo_create(me, me_oxs, "Cl", 1))
        elif len(comps) == 2:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
            elif "iSa" in comps[1].comp_type:
                iSaNo = comps[1]
            if "iOx" in comps[0].comp_type:
                iOxBa = comps[0]
            elif "iOx" in comps[1].comp_type:
                iOxBa = comps[1]
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxBa = comps[1]
                else:
                    iOxBa = comps[2]
            elif "iSa" in comps[1].comp_type:
                iSaNo = comps[1]
                if "iOx" in comps[0].comp_type:
                    iOxBa = comps[0]
                else:
                    iOxBa = comps[1]
            else:
                iSaNo = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxBa = comps[1]
                else:
                    iOxBa = comps[2]

        ((me1, me1_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        if me1_oxs == 1:
            return ""
        (me2, me2_oxs) = iOx_oxs(iOxBa.formula)
        if me1 != me2:
            return ""

        iSaBa = Compound(iSaBa_create(me1, me1_oxs, an, an_oxs))

        react = f"{iSaBa} -> {iSaNo} + {iOxBa} + H2O"

    return Reaction(react, "t ")

def r_3(comps: 'list(Compound)', is_input):
    """`iSaNo + (`iBaAlk_, `iBaBa_, `iBaAm_) -> `iSaBa"""
    react: str

    if is_input:
        iSaNo = Compound("CuCl2")
        iBa = Compound("Cu(OH)2")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                ((me, me_oxs), _) = iSa_oxs(iSaNo.formula)
                iBa = Compound(iBa_create(me, me_oxs))
            else:
                iBa = comps[0]
                (me, me_oxs) = iBa_oxs(iBa.formula)
                iSaNo = Compound(iSaNo_create(me, me_oxs, "Cl", 1))
        else:
            if "iSa" in comps[0].comp_type:
                iSaNo = comps[0]
                iBa = comps[1]
            else:
                iSaNo = comps[1]
                iBa = comps[0]

        ((me1, me1_oxs), (an, an_oxs)) = iSa_oxs(iSaNo.formula)
        (me2, me2_oxs) = iBa_oxs(iBa.formula)
        if me1 != me2:
            return ""
        if me1_oxs == 1:
            return ""

        iSaBa = Compound(iSaBa_create(me1, me1_oxs, an, an_oxs))

        react = f"{iSaNo} + {iBa} -> {iSaBa}"
    else:
        iSaBa = comps[0]

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iSaBa.formula)
        if me_oxs == 1:
            return ""

        iSaNo = Compound(iSaNo_create(me, me_oxs, an, an_oxs))
        iBa = Compound(iBa_create(me, me_oxs))

        react = f"{iSaNo} + {iBa} -> {iSaBa}"

    return Reaction(react)
