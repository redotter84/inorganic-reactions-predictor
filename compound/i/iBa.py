from copy import deepcopy

from element import Element
from tools.comps import index

# return (element, oxs) via base
def iBa_oxs(comp: 'Formula') -> (str):
    consist = deepcopy(comp.consist) # ElOH
    x_oxs = consist[Element("O")]

    del consist[Element("O")] # ElH
    del consist[Element("H")] # El

    x = list(consist.keys())[0].name
    if '[' in comp.value:
        if "(OH)" in comp.value:
            oh = comp.value.find("(OH)")
        else:
            oh = comp.value.find("OH")
        x = comp.value[0 : oh]

    return (x, int(x_oxs))

# return base via (element, oxs)
def iBa_create(x: str, x_oxs: int) -> (str): # El(OH){x_oxs}
    OH = "(OH)"
    if x_oxs == 1:
        OH = "OH"

    iBa = x + OH + index(x_oxs)
    return iBa
