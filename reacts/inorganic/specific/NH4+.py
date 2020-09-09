from compound import *
from compound.i.iAc import *
from compound.i.iSa import *
from reaction import *

def r_1(comps: 'list(Compound)', is_input):
    """`NH3` + (`iAcOx_, `iAcNox_) -> (`iSaAmm_, `iSaAmac_)"""
    react: str

    if is_input:
        iAc = Compound("HCl")
        if len(comps) == 1:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
        else:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
            else:
                iAc = comps[1]

        (an, an_oxs) = iAc_oxs(iAc.formula)

        iSaNH4 = Compound(iSaNo_create("Amm", 1, an, an_oxs))

        react = f"NH3 + {iAc} -> {iSaNH4}"
    else:
        iSaNH4 = comps[0]

        ((nh4, _), (an, an_oxs)) = iSa_oxs(iSaNH4.formula)
        if nh4 != "Amm":
            return ""

        iAc = Compound(iAc_create(an, an_oxs))

        react = f"NH3 + {iAc} -> {iSaNH4}"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """(`iSaAmm_, `iSaAmmAc_) -> `NH3` + (`iAcOx_, `iAcNox_)"""
    react: str

    if is_input:
        iSaNH4 = comps[0]

        (_, (an, an_oxs)) = iSa_oxs(iSaNH4.formula)
        if an == "NO3" or an == "NO2":
            return ""

        iAc = Compound(iAc_create(an, an_oxs))

        react = f"{iSaNH4} -> NH3 + {iAc}"
    else:
        iAc = Compound("HCl")
        if len(comps) == 1:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
        else:
            if "iAc" in comps[0].comp_type:
                iAc = comps[0]
            else:
                iAc = comps[1]

        (an, an_oxs) = iAc_oxs(iAc.formula)
        if an == "NO3" or an == "NO2":
            return ""

        iSaNH4 = Compound(iSaNo_create("Amm", 1, an, an_oxs))

        react = f"{iSaNH4} -> NH3 + {iAc}"

    return Reaction(react, "t ")
