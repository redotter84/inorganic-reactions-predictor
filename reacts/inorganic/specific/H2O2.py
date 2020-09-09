from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iAc import *
from compound.i.iSa import *
from reaction import *
from tools.comps import simple

# def r_1(comps: 'list(Compound)', is_input):
#     """`NH3` + (`iAcOx_, `iAcNox_) -> (`iSaAmm_, `iSaAmac_)"""
#     react: str
#
#     if is_input:
#         iAc = Compound("HCl")
#         if len(comps) == 1:
#             if "iAc" in comps[0].comp_type:
#                 iAc = comps[0]
#         else:
#             if "iAc" in comps[0].comp_type:
#                 iAc = comps[0]
#             else:
#                 iAc = comps[1]
#
#         (an, an_oxs) = iAc_oxs(iAc.formula)
#
#         iSaNH4 = Compound(iSaNo_create("Amm", 1, an, an_oxs))
#
#         react = f"NH3 + {iAc} -> {iSaNH4}"
#     else:
#         iSaNH4 = comps[0]
#
#         ((nh4, _), (an, an_oxs)) = iSa_oxs(iSaNH4.formula)
#         if nh4 != "Amm":
#             return ""
#
#         iAc = Compound(iAc_create(an, an_oxs))
#
#         react = f"NH3 + {iAc} -> {iSaNH4}"
#
#     return Reaction(react)
