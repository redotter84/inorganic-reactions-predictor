from database.elements.elements import *
from database.elements.oxs import *
from database.elements.react import *
from database.elements.weights import *

class Element:
    name: str # element name
    elem_type: str # element type, i.e. me or nonMe
    elem_sub_type: str # element subtype, e.g AlkMe, Hal

    # recognise the type of element
    def id_type(self):
        if self.name in db_nonMe:
            return "NonMe"
        elif self.name in db_in_el:
            return "In"
        else:
            return "Me"

    # recognise the subtype of element
    def id_sub_type(self):
        if self.elem_type == "Me":
            if self.name in db_AlkMe:
                return "AlkMe"
            elif self.name in db_AlkEMe:
                return "AlkEMe"
            else:
                return "Me"
        elif self.elem_type == "NonMe":
            if self.name in db_Hal:
                return "Hal"
            elif self.name in db_Noble:
                return "Noble"
            else:
                return "NonMe"
        elif self.elem_type == "In":
            return "In"

    # Element == Element
    def __eq__(self, el):
        return self.name == el.name

    # hash(Element)
    def __hash__(self):
        return hash(self.name)

    # constructor
    def __init__(self, value):
        self.name = value
        if self.name not in db_weights:
            raise Exception("Unknown element" + self.name)
        self.elem_type = self.id_type()
        self.elem_sub_type = self.id_sub_type()

# check is metal #1 activer than metal #2
def is_me_activer(me1, me1_oxs, me2, me2_oxs):
    f1 = 0
    if (me1, me1_oxs) in db_react: # if oxs is common
        f1 = db_react.index((me1, me1_oxs))
    elif (me1, 0) in db_react:
        f1 = db_react.index((me1, 0))
    else:
        return False
    f2 = 0
    if (me2, me2_oxs) in db_react: # if oxs is common
        f2 = db_react.index((me2, me2_oxs))
    elif (me2, 0) in db_react:
        f2 = db_react.index((me2, 0))
    else:
        return False
    return f1 < f2

def get_oxs(el):
    if el not in db_oxs:
        return 0
    return abs(max(db_oxs[el]))

def get_nme_oxs(nme):
    if nme not in db_oxs:
        return 0
    neg_oxs = [i for i in db_oxs[nme] if i < 0]
    if neg_oxs == []:
        return min(db_oxs[nme])
    return abs(max(neg_oxs))

def get_me_oxs(me):
    if me not in db_oxs:
        return 0
    pos_oxs = [i for i in db_oxs[me] if i > 0 and i < 5]
    if pos_oxs == []:
        return 0
    return min(pos_oxs)
