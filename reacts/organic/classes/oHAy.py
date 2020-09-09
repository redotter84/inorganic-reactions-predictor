from compound import *
from compound.o.oH import *
from reaction import *

def r_1(comps: 'list(Compound)', is_input):
    """`oHAy + `H2` -> `oHAa"""
    react: str

    if is_input:
        oHAy = Compound("CH#CH")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAy = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAy = comps[0]
            else:
                oHAy = comps[1]

        (n, _) = oHAy_parse(oHAy.skeleton)

        oHAa = Compound(oHAa_create(n))

        react = f"{oHAy} + H2 -> {oHAa}"
    else:
        oHAa = comps[0]

        if oHAa.skeleton.value == "CH4":
            return ""
        n = oHAa_parse(oHAa.skeleton)

        oHAy = Compound(oHAy_create(n))

        react = f"{oHAy} + H2 -> {oHAa}"

    return Reaction(react, "c: Pt")

def r_2(comps: 'list(Compound)', is_input):
    """`oHAy + `H2` -> `oHAe"""
    react: str

    if is_input:
        oHAy = Compound("CH#CH")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAy = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAy = comps[0]
            else:
                oHAy = comps[1]

        (n, _) = oHAy_parse(oHAy.skeleton)

        oHAe = Compound(oHAe_create(n))

        react = f"{oHAy} + H2 -> {oHAe}"
    else:
        oHAe = comps[0]

        (n, _) = oHAe_parse(oHAe.skeleton)

        oHAy = Compound(oHAy_create(n))

        react = f"{oHAy} + H2 -> {oHAe}"

    return Reaction(react, "c: Pt")
