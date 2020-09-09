from compound.i.iOx import iOx_oxs
from compound.i.iBa import iBa_oxs
from database.compounds.iOx import *
from database.compounds.iBa import *
from element import Element
from formula import *
from tools.comps import index, simple
from tools.container import key_in_dict

def id_inorganic_type(comp):
    formula = comp.formula

    isAlkMe = lambda el: el.elem_sub_type == "AlkMe" \
      or el.elem_sub_type == "AlkEMe"
    isMe = lambda el: el.elem_type == "Me"
    isNonMe = lambda el: el.elem_type == "NonMe"

    if Element("Bz") in formula.consist:
        return "nil"

    def id_iWa(): # water
        if formula.value == "H2O":
            return "iWa"

    def id_iSi(): # simple compound
        if len(formula.consist) != 1:
            return ""

        elem = list(formula.consist.keys())[0]
        if elem.name == "O":
            if formula.value not in ["[O]", "O2", "O3"]:
                return "nil"
        elif formula.value != simple(elem.name):
            return "nil"

        if elem.elem_type == "Me": # metal
            return "iSiMe"
        elif elem.elem_type == "NonMe": # non-metal
            return "iSiNme"
        else:
            return "nil"

    def id_iOx(): # oxide
        if len(formula.consist) != 2:
            return ""
        if Element("O") not in formula.consist:
            return ""
        if Element("F") in formula.consist: # OF2 is not oxide
            return ""
        if formula.value == "H2O2":
            return "nil"
        if formula.value in db_peroxides:
            return "iSaPer"

        def id_iOxAlk(): # alkaline oxide
            if key_in_dict(formula.consist, isAlkMe):
                return "iOxAlk"

        def id_iOxBa(): # basic oxide
            if not key_in_dict(formula.consist, isMe):
                return ""
            _, oxs = iOx_oxs(formula)
            if (oxs <= 2 and formula.value not in db_iOxAm) \
              or formula.value in db_iOxBa:
                return "iOxBa"

        def id_iOxAc(): # acidic oxide
            if not (key_in_dict(formula.consist, isNonMe)-1):
                _, oxs = iOx_oxs(formula)
                if oxs < 5:
                    return ""
            return "iOxAc"

        def id_iOxAm(): # amphoteric oxide
            return "iOxAm"

        def id_iOxNs(): # non salt formating oxide
            if formula.value in db_iOxNs:
                return "iOxNs"

        sub_fns = [id_iOxNs, id_iOxAlk, id_iOxBa, id_iOxAc, id_iOxAm]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return ""

    def id_iBa(): # base
        if "OH" not in formula.value:
            return ""
        if key_in_dict(formula.consist, isNonMe) > 2 and \
           '[' not in formula.value:
            return ""
        if formula.value.find("OH") < formula.value.find("]"):
            return ""
        if formula.value == "AmmOH":
            return "nil"

        def id_iBaCo(): # complex base
            if "]OH" in formula.value:
                return "iBaCo"
            elif "](OH)" in formula.value:
                return "iBaCo"

        def id_iBaAlk(): # alkaline
            if key_in_dict(formula.consist, isAlkMe):
                return "iBaAlk"

        def id_iBaBa(): # base
            _, oxs = iBa_oxs(formula)
            if (oxs <= 2 and formula.value not in db_iBaAm) \
              or formula.value in db_iBaBa:
                return "iBaBa"

        def id_iBaAm(): # amphoteric base
            return "iBaAm"

        sub_fns = [id_iBaCo, id_iBaAlk, id_iBaBa, id_iBaAm]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return ""

    def id_iAc(): # acid
        if formula.value[0] != "H":
            return ""
        if formula.value == "H2O2":
            return ""
        if Element("H") not in formula.consist:
            return ""
        if Element("C") in formula.consist:
            if formula.value not in ["H2CO3", "HCN", "HCNO"]:
                return "nil"
        if key_in_dict(formula.consist, isMe) \
          and len(formula.consist) < 3:
            return ""

        def id_iAcOx(): # acid with oxygen
            if Element("O") in formula.consist:
                return "iAcOx"

        def id_iAcNox(): # acid without oxygen
            return "iAcNox"

        def id_iAcCo(): # complex base
            if '[' in formula.value:
                return "iAcCo"

        sub_fns = [id_iAcCo, id_iAcOx, id_iAcNox]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                val = formula.value
                pos = 0
                while val[pos] == 'H':
                    pos += 1
                val = "H" + index(pos) + val[pos : ]
                comp.formula = Formula(val)
                return comp_type
        return ""

    def id_iSa(): # salt
        if not key_in_dict(formula.consist, isNonMe):
            return ""
        if not key_in_dict(formula.consist, isMe):
            return ""
        if Element("H") in formula.consist and len(formula.consist) < 3:
            return ""
        if len(formula.consist) == 2:
            if Element("C") in formula.consist or \
               Element("N") in formula.consist or \
               Element("Si") in formula.consist:
               return ""
        if Element("C") in formula.consist:
            if "CO3" not in formula.value and \
               "CN" not in formula.value and "CNO" not in formula.value:
                return ""

        def id_iSaCo(): # complex salt
            if '[' in formula.value:
                return "iSaCo"

        def id_iSaNo(): # normal salt
            return "iSaNo"

        def id_iSaBa(): # basic salt
            if "OH" in formula.value:
                return "iSaBa"

        def id_iSaAc(): # acidic salt
            if Element("H") in formula.consist:
                return "iSaAc"

        def id_iSaAmm():
            if Element("Amm") in formula.consist:
                return "iSaAmm"

        def id_iSaAmmAc():
            if Element("Amm") in formula.consist \
              and Element("H") in formula.consist:
                return "iSaAac"

        sub_fns = [id_iSaCo, id_iSaAmmAc, id_iSaAmm, id_iSaBa, id_iSaAc, id_iSaNo]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return ""

    def id_iBi():
        if len(formula.consist) != 2:
            return ""
        if Element("C") in formula.consist:
            if list(formula.consist.keys())[0].elem_type != "Me" and \
               list(formula.consist.keys())[1].elem_type != "Me":
               return ""
        if list(formula.consist.keys())[0].elem_type == "In" or \
           list(formula.consist.keys())[1].elem_type == "In":
           return ""
        return "iBi"

    fns = [id_iWa, id_iSi, id_iOx, id_iBa, id_iAc, id_iSa, id_iBi]
    for fn in fns:
        comp_type = fn()
        if comp_type:
            return comp_type
    return "nil"
