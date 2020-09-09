from copy import deepcopy

from element import Element
from tools.comps import chain
from tools.container import flatten

def id_organic_type(comp):
    formula = comp.formula
    skeleton = comp.skeleton
    subst = []
    for s in comp.skeleton.subst:
        subst += s

    if Element("C") not in formula.consist and Element("Bz") not in formula.consist:
        return "nil"

    def id_oH():
        if Element("H") not in formula.consist:
            return ""
        if len(formula.consist) == 3:
            if Element("C") not in formula.consist or \
               Element("Bz") not in formula.consist:
                return ""
        elif len(formula.consist) != 2:
            return ""

        c = -1
        h = -1
        if Element("C") in formula.consist:
            c = formula.consist[Element("C")]
            h = formula.consist[Element("H")]

        def id_oHAa():
            if h == 2 * c + 2 and "-" in skeleton.value:
                return "oHAa"
            if formula.value == "CH4":
                return "oHAa"

        def id_oHAe():
            if h == 2 * c and "=" in skeleton.value and \
               "{" not in skeleton.value:
                return "oHAe"

        def id_oHAy():
            if h == 2 * c - 2 and \
               "=" not in skeleton.value and "#" in skeleton.value and \
               "{" not in skeleton.value:
               return "oHAy"

        def id_oHDi():
            if h == 2 * c - 2 and skeleton.value.count("=") == 2:
                return "oHDi"

        def id_oHCa():
            if h == 2 * c and c > 3 and "{" in skeleton.value:
                return "oHCa"

        def id_oHAr():
            if Element("Bz") in formula.consist:
                return "oHAr"

        sub_fns = [id_oHAa, id_oHAe, id_oHAy, id_oHDi, id_oHCa, id_oHAr]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return "oH*"

    def id_oHal():
        for el in formula.consist:
            if el.name not in ["C", "H"] and el.elem_sub_type != "Hal":
                return ""
        return "oHal"

    def id_oO():
        if Element("H") not in formula.consist or Element("O") not in formula.consist:
            return ""
        if len(formula.consist) == 4:
            if Element("Bz") not in formula.consist:
                return ""
        elif len(formula.consist) != 3:
            return ""

        def id_oOAc():
            if "O" not in subst or "OH" not in subst:
                return ""
            return "oOAc"

        def id_oOAlc():
            if "OH" not in subst:
                return ""
            if Element("Bz") in formula.consist:
                return "oOPh"
            else:
                return "oOAlc"

        def id_oOAld():
            if len(subst) < 2:
                return ""
            if subst[-1] == "HO":
                return "oOAld"

        def id_oOKet():
            if skeleton.skeleton.count("C") < 3:
                return ""
            if "O" in subst:
                if subst.index("O") > 2 and subst.index("O") < len(subst) - 3:
                    return "oOKet"

        def id_oOEth():
            if "-O-" in skeleton.skeleton:
                return "oOEth"

        sub_fns = [id_oOAc, id_oOAlc, id_oOAld, id_oOKet, id_oOEth]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return "oO*"

    def id_oN():
        if Element("N") not in formula.consist:
            return ""

        def id_oNAc():
            if Element("H") not in formula.consist or \
               Element("O") not in formula.consist:
                return ""
            if len(formula.consist) == 5:
                if Element("Bz") not in formula.consist:
                    return ""
            elif len(formula.consist) != 4:
                return ""

            if "O" not in flatten(subst) or "OH" not in flatten(subst) or \
               "NHH" not in flatten(subst):
                return ""
            return "oNAc"

        def id_oNAm():
            if Element("H") not in formula.consist:
                return ""
            if len(formula.consist) == 4:
                if Element("C") not in formula.consist or \
                   Element("Bz") not in formula.consist:
                    return ""
            elif len(formula.consist) != 3:
                return ""

            if "NH" not in skeleton.value and "N(#" not in skeleton.value:
               return ""
            return "oNAm"

        def id_oNNi():
            if "NOO" in flatten(skeleton.subst):
                return "oNNi"

        sub_fns = [id_oNAc, id_oNAm, id_oNNi]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return "oN*"

    def id_oS():
        if Element("S") not in formula.consist:
            return ""

        sub_fns = []
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return "oS*"

    def id_oP():
        if Element("P") not in formula.consist:
            return ""

        sub_fns = []
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return "oP*"

    def id_oHe():
        he = False
        for el in formula.consist:
            if el.name not in ["C", "O", "H", "N", "P", "S"] and \
               el.elem_sub_type != "Hal":
               he = True
        if not he:
            return ""

        sub_fns = []
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type
        return "oHe_"

    def id_oBio():
        if Element("O") not in formula.consist or \
           Element("H") not in formula.consist:
            return ""
        if len(formula.consist) != 3:
            return ""

        def id_oBioHy():
            c: int
            if Element("Bz") in formula.consist:
                c = formula.consist[Element("Bz")] * 6
            else:
                c = formula.consist[Element("C")]

            h = formula.consist[Element("H")]
            o = formula.consist[Element("O")]
            if c < 4 or o < 4:
                return ""
            if h == 2 * o:
                return "oBioWa"

        def id_oBioLi():
            if Element("Bz") in formula.consist:
                return ""
            if len(formula.consist) != 3:
                return ""
            if chain(skel.value) == "CH2-CH-CH2":
                return "oBioLi"

        sub_fns = [id_oBioHy, id_oBioLi]
        for fn in sub_fns:
            comp_type = fn()
            if comp_type:
                return comp_type

    fns = [id_oH, id_oHal, id_oP, id_oS, id_oN, id_oO, id_oBio, id_oHe]
    for fn in fns:
        comp_type = fn()
        if comp_type:
            return comp_type
    return "nil"
