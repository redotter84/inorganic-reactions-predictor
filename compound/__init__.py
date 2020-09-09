from formula import *
from formula.skeleton import *
from compound.inorganic import *
from compound.organic import *

# class for inorganic compound
class Compound:
    formula: 'Formula' # formula of the compound
    comp_type: str # type of compound
    skeleton: 'Skeleton'

    def replace_name(self, val):
        value = val

        value = value.replace("NH4", "Amm").replace("(Amm)", "Amm")
        value = value.replace("C6", "Bz")
        if val == "H4C":
            value = "CH4"
        elif val == "H3N":
            value = "NH3"
        elif val == "H4Si":
            value = "SiH4"
        elif val == "HO":
            value = "H2O2"

        value = value.replace("-", "").replace("=", "").replace("#", "").\
                replace("{", "").replace("}", "")

        return value

    def __str__(self):
        str_val: str
        if self.comp_type[0] == "o":
            str_val = self.skeleton.value
        else:
            str_val = self.formula.value
        for i in range(1, 10):
            str_val = str_val.replace(f"Amm{i}", f"(NH4){i}")
        str_val = str_val.replace("Amm", "NH4")
        return str_val

    def __repr__(self):
        str_val = str(self)
        str_val = str_val.replace("-", "–").replace("#", "≡")
        for i in range(0, 10):
            str_val = str_val.replace(f"{i}", chr(0x2080 + i))
        str_val = str_val.replace("Bz", "\u23e3")
        return str_val

    # constructor
    def __init__(self, value: str):
        open_value = self.replace_name(value)
        self.formula = Formula(open_value)
        self.comp_type = id_inorganic_type(self)
        if self.comp_type == "nil":
            self.skeleton = Skeleton(value)
            self.comp_type = id_organic_type(self)
