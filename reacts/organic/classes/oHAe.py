from compound import *
from compound.o.oH import *
from reaction import *

def r_1(comps: 'list(Compound)', is_input):
    """`oHAe + `H2` -> `oHAa"""
    react: str

    if is_input:
        oHAe = Compound("CH2=CH2")
        if len(comps) == 1:
            if "oH" in comps[0].comp_type:
                oHAe = comps[0]
        else:
            if "oH" in comps[0].comp_type:
                oHAe = comps[0]
            else:
                oHAe = comps[1]

        (n, _) = oHAe_parse(oHAe.skeleton)

        oHAa = Compound(oHAa_create(n))

        react = f"{oHAe} + H2 -> {oHAa}"
    else:
        oHAa = comps[0]

        if oHAa.skeleton.value == "CH4":
            return ""
        n = oHAa_parse(oHAa.skeleton)

        oHAe = Compound(oHAe_create(n))

        react = f"{oHAe} + H2 -> {oHAa}"

    return Reaction(react, "c: Pt")
