from compound.o.oH import *

db_gases = ["H2", "He", "N2", "O2", "O3", "F2", "Cl2", "Ne", "Ar", "Kr", "Xe", "Og", "NH3", "SiH4", "CO", "CO2", "N2O", "NO", "NO2", "SO2", "H2S", "CH2=C=CH2", "CH2=CH-CH=CH2"]

def is_gase(comp: 'Compound'):
    if comp.formula.value in db_gases:
        return True

    elif comp.comp_type[0] == 'o':
        if comp.skeleton.value in db_gases:
            return True
        if comp.comp_type == "oHAa":
            return oHAa_parse(comp.skeleton) <= 4
        elif comp.comp_type == "oHAe":
            return oHAe_parse(comp.skeleton)[0] <= 4
        elif comp.comp_type == "oHAy":
            return oHAy_parse(comp.skeleton)[0] <= 4
        elif comp.comp_type == "oHCa":
            return oHCa_parse(comp.skeleton) <= 4
        else:
            return False

    else:
        return False
