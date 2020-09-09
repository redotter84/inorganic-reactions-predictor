from compound import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from database.compounds.solubility import *
from database.elements.binary import *
from element import *
from reaction import *
from tools.comps import simple

def r_1(comps: 'list(Compound)', is_input):
    """(`iSiMe_, `iSiNme_) + (`iSiMe__, `iSiNme__) ->"""\
    """(`iSaNo_, `iBi_, `iAcNox_, `CH4`_)"""
    react: str

    if is_input:
        iSiMe = Compound("Na")
        iSiNme = Compound("H2")
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
        nme = list(iSiNme.formula.consist.keys())[0].name
        if Element(me).elem_type == "NonMe":
            if is_me_activer(nme, 0, me, 0):
                iSiNme, iSiMe = iSiMe, iSiNme
                me = list(iSiMe.formula.consist.keys())[0].name
                nme = list(iSiNme.formula.consist.keys())[0].name

        me_oxs = get_me_oxs(me)
        if Element(me).elem_type == "NonMe":
            me_oxs = get_oxs(me)
        if me_oxs == 0:
            return ""

        nme_oxs = get_nme_oxs(nme)
        if nme_oxs == 0:
            return ""
        if nme in ["O"]:
            return ""

        Me = Element(me)
        Nme = Element(nme)
        if Me.elem_type == "Me" and Nme.elem_type == "NonMe":
            if Nme.elem_sub_type != "Hal" and \
               nme not in ["H", "B", "C", "N", "Si", "P", "S"]:
                if Me.elem_sub_type != "AlkMe":
                   return ""
            elif nme in ["H", "B", "C", "N", "Si", "P", "S"]:
                if is_me_activer("Al", 3, me, me_oxs):
                    return ""

        if nme in db_not_bin:
            if me in db_not_bin[nme]:
                return ""

        iBi = Compound(iSaNo_create(me, me_oxs, nme, nme_oxs))
        if me == "O" and nme == "F":
            iBi = Compound("O2F2")

        react = f"{iSiMe} + {iSiNme} -> {iBi}"
    else:
        iBi = comps[0]

        if len(iBi.formula.consist) != 2:
            return ""

        ((me, me_oxs), (nme, _)) = iSa_oxs(iBi.formula)
        if me == "H" and nme == "C":
            return ""

        Me = Element(me)
        Nme = Element(nme)
        if Me.elem_type == "Me" and Nme.elem_type == "NonMe":
            if Nme.elem_sub_type != "Hal" and \
               nme not in ["H", "B", "C", "N", "Si", "P", "S"]:
                if Me.elem_sub_type != "AlkMe":
                   return ""
            elif nme not in ["H", "B", "C", "N", "Si", "P", "S"]:
                if is_me_activer("Al", 3, me, me_oxs):
                    return ""

        if nme in db_not_bin:
            if me in db_not_bin[nme]:
                return ""

        iSiMe = Compound(simple(me))
        iSiNme = Compound(simple(nme))

        react = f"{iSiMe} + {iSiNme} -> {iBi}"

    return Reaction(react, "t ")

def r_2(comps: 'list(Compound)', is_input):
    """(`iBi_, `iSaNo_, `iAcNox_, `CH4`_) ->"""\
    """(`iSiMe_, `iSiNme_) + (`iSiMe__, `iSiNme__)"""
    react: str

    if is_input:
        iBi = comps[0]

        if len(iBi.formula.consist) != 2:
            return ""

        ((me, _), (nme, _)) = iSa_oxs(iBi.formula)

        iSiMe = Compound(simple(me))
        iSiNme = Compound(simple(nme))

        react = f"{iBi} -> {iSiMe} + {iSiNme}"
    else:
        iSiMe = Compound("H2")
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
        nme = list(iSiNme.formula.consist.keys())[0].name
        if is_me_activer(nme, 0, me, 0):
            iSiNme, iSiMe = iSiMe, iSiNme
            me = list(iSiMe.formula.consist.keys())[0].name
            nme = list(iSiNme.formula.consist.keys())[0].name

        me_oxs = get_me_oxs(me)
        if Element(me).elem_type == "NonMe":
            me_oxs = get_oxs(me)
        if me_oxs == 0:
            return ""

        nme_oxs = get_nme_oxs(nme)
        if nme_oxs == 0:
            return ""
        if nme in ["O"]:
            return ""

        iBi = Compound(iSaNo_create(me, me_oxs, nme, nme_oxs))
        if me == "O" and nme == "F":
            iBi = Compound("O2F2")
        if iBi.formula.value == "HH":
            return ""

        react = f"{iBi} -> {iSiMe} + {iSiNme}"

    return Reaction(react, "t ")

def r_3(comps: 'list(Compound)', is_input):
    """(`iBi_, `iSaNo_, `iSaPer_) + `iWa ->"""\
    """(`iBaAlk, `iBaBa_, `iBaAm_) + (`iAcNox__, `iAcOx__, `iBi__, `CH4`__, `H2O2`__)"""
    react: str

    if is_input:
        iBi = Compound("Al2S3")
        if len(comps) == 1:
            if "iBi" in comps[0].comp_type or "iSa" in comps[0].comp_type:
                iBi = comps[0]
        else:
            if "iBi" in comps[0].comp_type or "iSa" in comps[0].comp_type:
                iBi = comps[0]
            else:
                iBi = comps[1]

        if len(iBi.formula.consist) != 2:
            return ""

        ((me, me_oxs), (an, an_oxs)) = iSa_oxs(iBi.formula)
        if Element(me).elem_type == "Me" and Element(an).elem_type == "Me":
            return ""

        if iBi.comp_type not in ["iBi", "iSaPer"]:
            if (me, me_oxs) not in db_hydr:
                return ""
            if an not in db_hydr[(me, me_oxs)]:
                return ""

        iBa = Compound(iBa_create(me, me_oxs))
        iAc = Compound(iAc_create(an, an_oxs))
        if "iBa" not in iBa.comp_type:
            return ""

        react = f"{iBi} + H2O -> {iBa} + {iAc}"
    else:
        iBa = Compound("Al(OH)3")
        iAc = Compound("H2S")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type:
                iBa = comps[0]
            else:
                iAc = comps[0]
                if iAc.formula.value == "H2O2":
                    iBa = Compound("NaOH")
        else:
            if "Ba" in comps[0].comp_type:
                iBa = comps[0]
                iAc = comps[1]
            else:
                iBa = comps[1]
                iAc = comps[0]

        if Element("H") not in iAc.formula.consist:
            return ""

        (me, me_oxs) = iBa_oxs(iBa.formula)
        (an, an_oxs) = iAc_oxs(iAc.formula)
        if iAc.comp_type == "iBi" or iAc.formula.value == "CH4":
            (an, an_oxs) = iAc_el_oxs(iAc.formula)
        if an == "C" and iAc.formula.value != "CH4":
            return ""

        if iAc.comp_type == "iBi" and \
           Element(me).elem_type == "Me" and Element(an).elem_type == "Me":
            return ""

        iBi = Compound(iSaNo_create(me, me_oxs, an, an_oxs))
        if iBi.comp_type not in ["iBi", "iSaPer"]:
            if (me, me_oxs) not in db_hydr:
                return ""
            if an not in db_hydr[(me, me_oxs)]:
                return ""

        react = f"{iBi} + H2O -> {iBa} + {iAc}"

    return Reaction(react)
