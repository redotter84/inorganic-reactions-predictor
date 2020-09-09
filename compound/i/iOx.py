from copy import deepcopy

from element import Element
from tools.comps import index

# return (element, oxs) via oxide
def iOx_oxs(comp: 'Formula') -> (str, int):
    consist = deepcopy(comp.consist) # ElO
    o_q = consist[Element("O")]
    del consist[Element("O")] # El
    x = list(consist.keys())[0]
    x_q = consist[x]
    x_oxs = o_q * 2 / x_q

    return (x.name, int(x_oxs))

# return oxide via (element, oxs)
def iOx_create(x: str, x_oxs: int) -> (str): # El{x_q}O{o_q}
    x_q = 1 + x_oxs % 2
    o_q = int(x_q * x_oxs / 2)

    iOx = x + index(x_q) + "O" + index(o_q)
    return iOx
