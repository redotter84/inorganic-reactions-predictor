from compound.i.iSa import iSa_oxs
from compound.o.oH import *
from element import Element

db_hydr = {
    ("Al", 3): ["CO3", "S", "SO3", "SiO3"],
    ("Be", 2): ["CO3", "S", "SiO3"],
    ("Cr", 2): ["CO3", "S", "CO3"],
    ("Cr", 3): ["CO3", "S", "SO3", "SiO3"],
    ("Cu", 2): ["CO3", "SiO3"],
    ("Fe", 3): ["CO3", "S", "SO3", "SiO3"],
    ("Hg", 2): ["CO3", "SiO3"],
    ("Mg", 2): ["CO3", "S", "SiO3"],
}

# solubility table (insoluble compounds)
db_table = {
    ("Ag", 1): ["Br", "CO3", "Cl", "I", "PO4", "S", "SO3", "SiO3"],
    ("Al", 3): ["PO4"],
    ("Ba", 2): ["CO3", "PO4", "SO3", "SO4", "SiO3"],
    ("Be", 2): ["PO4", "SO3"],
    ("Ca", 2): ["F", "CO3", "PO4", "S", "SO3", "SiO3"],
    ("Cd", 2): ["CO3", "PO4", "S", "SO3", "SiO3"],
    ("Co", 2): ["S", "SO3", "PO4", "CO3", "SiO3"],
    ("Cr", 2): ["F", "PO4", "SiO3"],
    ("Cr", 3): ["PO4"],
    ("Cs", 1): ["ClO4"],
    ("Cu", 2): ["F", "I", "S", "SO3", "PO4"],
    ("Fe", 2): ["CO3", "F", "S", "PO4", "SO3", "SiO3"],
    ("Fe", 3): ["PO4"],
    ("Hg", 2): ["F", "I", "PO4", "S", "SO3"],
    ("K", 1):  ["ClO4", "[PtCl6]"],
    ("Li", 1): ["CO3", "F", "PO4"],
    ("Mg", 2): ["F", "PO4", "SO3"],
    ("Mn", 2): ["CO3", "F", "PO4", "S", "SO3", "SiO3"],
    ("Na", 1): ["[BeF4]", "BiO3"],
    ("Ni", 2): ["CO3", "PO4", "S", "SO3", "SiO3"],
    ("Pb", 2): ["CO3", "PO4", "F", "I", "S", "SO3", "SO4", "SiO3"],
    ("Rb", 1): ["ClO4", "[PtCl6]"],
    ("Sn", 2): ["PO4", "S"],
    ("Sr", 2): ["F", "CO3", "PO4", "SO4"],
    ("Zn", 2): ["CO3", "PO4", "S", "SiO3"]
}

# check is compound soluble (for exchange reactions too)
def is_ionic_soluble(comp: 'Compound'):
    if comp.comp_type[0] == 'i':
        if "iSi" in comp.comp_type:
            el = list(comp.formula.consist.keys())[0]
            return el.elem_sub_type != "Me"

        elif "iOx" in comp.comp_type:
            return comp.comp_type not in ["iOxBa", "iOxAm"]

        if "iBa" in comp.comp_type:
            return comp.comp_type in ["iBaAlk", "iBaCo"] or comp.formula.value == "AmmOH"

        elif "iAc" in comp.comp_type:
            return comp.formula.value not in ["H2SiO3", "H3BO3"]

        elif "iSa" in comp.comp_type:
            if comp.comp_type == "iSaNo" or comp.comp_type == "iSaCo":
                ((kat, kat_oxs), (an, _)) = iSa_oxs(comp.formula)
                if (kat, kat_oxs) in db_table and an in db_table[(kat, kat_oxs)]:
                    return False
                if (kat, kat_oxs) in db_hydr and an in db_hydr[(kat, kat_oxs)]:
                    return False
                elif "[" not in kat and Element(kat).elem_sub_type == "AlkMe":
                    return True
                elif kat == "Amm":
                    return True
                elif an == "NO3":
                    return True
                elif an == "ClO4":
                    return True
                elif an in ["S", "SO3", "PO4", "CO3", "SiO3"]:
                    return False
                else:
                    return True
            elif comp.comp_type == "iSaAc":
                return True
            elif comp.comp_type == "iSaBa":
                return True
            else:
                return True

        elif "iBi" in comp.comp_type:
            return True

        else:
            return True

    elif comp.comp_type[0] == 'o':
        if comp.comp_type == "oHAa":
            return oHAa_parse(comp.skeleton) < 18
        elif comp.comp_type == "oHAe":
            return oHAe_parse(comp.skeleton)[0] < 17
        elif comp.comp_type == "oHAy":
            return oHAy_parse(comp.skeleton)[0] < 16
        elif comp.comp_type == "oHDi":
            return oHAy_parse(comp.skeleton)[0] < 15
        elif comp.comp_type == "oHCa":
            return oHCa_parse(comp.skeleton) < 12
        else:
            return True

    else:
        return True
