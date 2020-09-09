from compound import Compound
from tools.container import find_if
from database.compounds.solubility import *
from database.compounds.gases import *

# check if reaction is exchange
def is_exchange(r_out: 'list(Compound)') -> (bool):
    if Compound("H2O") in r_out: # water
        return True
    elif find_if(r_out, lambda c: is_gase(c)) != -1: # gases
        return True
    elif find_if(r_out, lambda c: not is_ionic_soluble(c)) != -1: # insoluble
        return True
    else:
        return False
