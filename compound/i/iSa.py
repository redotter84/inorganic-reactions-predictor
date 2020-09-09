from copy import deepcopy

from compound import *
from database.compounds.iAc import db_anions
from database.elements.oxs import db_oxs
from element import *
from formula import *
from tools.comps import index
from tools.container import count_if, find_if
from tools.math import lcm

def _iSaNo_oxs(salt): # MeAn
    val = salt.formula.value
    is_dig_up_br = lambda c: c.isdigit() or c.isupper() or c == "("

    me: str; me_q: int; me_oxs: int
    anion: str; an_q: int; an_oxs: int

    me_end_pos = find_if(val[1 : ], is_dig_up_br)
    me = val[0 : me_end_pos + 1]

    consist = deepcopy(salt.formula.consist)
    me_q = consist[Element(me)]
    del consist[Element(me)]

    an_beg_pos = find_if(val[1 : ], lambda c: c.isupper()) + 1
    an_end_pos = find_if(val[an_beg_pos : ], \
      lambda c: c == ')') + an_beg_pos
    if an_end_pos == an_beg_pos - 1:
        an_end_pos = len(val)
    anion = val[an_beg_pos : an_end_pos] # An

    an = Compound(anion)
    if len(an.formula.consist) == 1: # MeNm
        anion = list(an.formula.consist.keys())[0].name
        an = Compound(anion)

    nonme = list(consist.keys())[0]
    an_q = int(consist[nonme] / an.formula.consist[nonme])

    if anion in db_anions:
        an_oxs = db_anions[anion]
        me_oxs = an_oxs * an_q / me_q
    elif me in db_oxs and db_oxs[me] != [0]:
        me_oxs = get_me_oxs(me)
        an_oxs = me_oxs * me_q / an_q
    else:
        me_oxs = 1
        an_oxs = me_oxs * me_q / an_q

    return ((me, int(me_oxs)), (anion, int(an_oxs)))

def _iSaAc_oxs(salt): # MeHAn
    val = salt.formula.value
    is_dig_up_br = lambda c: c.isdigit() or c.isupper() or c == "("

    me: str; me_q: int; me_oxs: int
    h_q: int
    anion: str; an_q: int; an_oxs: int

    me_end_pos = find_if(val[1 : ], is_dig_up_br)
    me = val[0 : me_end_pos + 1]

    consist = deepcopy(salt.formula.consist)
    me_q = consist[Element(me)]
    del consist[Element(me)]
    h_q = consist[Element("H")]
    del consist[Element("H")]

    anh_beg_pos = find_if(val[1 : ], lambda c: c.isupper()) + 1
    anh_end_pos = find_if(val[anh_beg_pos : ],
      lambda c: c == ')') + anh_beg_pos
    if anh_end_pos == anh_beg_pos - 1:
        anh_end_pos = len(val)
    anionh = val[anh_beg_pos : anh_end_pos] # HAn

    an_beg_pos = find_if(anionh[1 : ], lambda c: c.isupper()) + 1
    an_end_pos = find_if(anionh[an_beg_pos : ],
      lambda c: c == ')') + an_beg_pos
    if an_end_pos == an_beg_pos - 1:
        an_end_pos = len(val)
    anion = anionh[an_beg_pos : an_end_pos] # An

    an = Compound(anion)
    if len(an.formula.consist) == 1: # MeNm
        anion = list(an.formula.consist.keys())[0].name
        an = Compound(anion)
    nonme = list(consist.keys())[0]
    an_q = int(consist[nonme] / an.formula.consist[nonme])

    if anion in db_anions:
        an_oxs = db_anions[anion]
        me_oxs = (an_oxs * an_q - h_q) / me_q
    elif me in db_oxs and db_oxs[me] != [0]:
        me_oxs = get_me_oxs(me)
        an_oxs = (me_oxs * me_q + h_q) / an_q
    else:
        me_oxs = 1
        an_oxs = (me_oxs * me_q + h_q / an_q)

        anion = "H" + index(_h_q) + anion

    return ((me, int(me_oxs)), (anion, int(an_oxs)))

def _iSaBa_oxs(salt): # MeOHAn
    val = salt.formula.value
    is_dig_up_br = lambda c: c.isdigit() or c.isupper() or c == "("

    me: str; me_q: int; me_oxs: int
    oh_q: int
    anion: str; an_q: int; an_oxs: int

    if val[0] != '(': # MeOHAn
        me_end_pos = find_if(val[1 : ], is_dig_up_br) + 1
        me = val[0 : me_end_pos]
    else: # (MeOH)An
        me_end_pos = find_if(val[2 : ], is_dig_up_br) + 2
        me = val[1 : me_end_pos]

    oh = val.find("OH")
    oh_end_pos = find_if(val[oh : ], is_dig_up_br) + 1

    consist = deepcopy(salt.formula.consist)
    me_q = consist[Element(me)]
    del consist[Element(me)]

    oh_q = consist[Element("H")]
    del consist[Element("H")]

    an_cont = val[oh + oh_end_pos : ] # )An
    an_beg_pos = find_if(an_cont[1 : ], lambda c: c.isupper()) + 1
    an_end_pos = find_if(an_cont[an_beg_pos : ], \
      lambda c: c == ')') + an_beg_pos
    if an_end_pos == an_beg_pos - 1:
        an_end_pos = len(an_cont)
    anion = an_cont[an_beg_pos : an_end_pos] # An

    an = Compound(anion)
    if len(an.formula.consist) == 1: # MeNm
        anion = list(an.formula.consist.keys())[0].name
        an = Compound(anion)
        nonme = Element(anion)
    elif Element("O") in an.formula.consist: # MeNmO
        an_cons = deepcopy(an.formula.consist)
        del an_cons[Element("O")]
        nonme = list(an_cons.keys())[0]
    else: # MeNmNm
        nonme = list(consist.keys())[0]
    an_q = int(consist[nonme] / an.formula.consist[nonme])

    if anion in db_anions:
        an_oxs = db_anions[anion]
        me_oxs = (an_oxs * an_q + oh_q) / me_q
    elif me in db_oxs and db_oxs[me] != [0]:
        me_oxs = get_me_oxs(me)
        an_oxs = (me_oxs * me_q - oh_q) / an_q
    else:
        me_oxs = 1
        an_oxs = (me_oxs * me_q - oh_q) / an_q

    return ((me, int(me_oxs)), (anion, int(an_oxs)))

def _iSaCo_oxs(salt):
    val = salt.formula.value

    op1 = val.find('[')
    cl1 = val.find(']') + 1
    br1 = val[op1 : cl1]
    if op1 == 0:
        val = val.replace(br1, "Kat")
    else:
        val = val.replace(br1, "An")

    op2 = val.find('[')
    cl2 = val.find(']') + 1
    br2: str
    if op2 != -1:
        br2 = val[op2 : cl2]
        val = val.replace(br2, "An")

    ((k, k_oxs), (a, a_oxs)) = iSa_oxs(Formula(val))
    if k == "Kat":
        k = br1
        if a == "An":
            a = br2
    elif a == "An":
        a = br1

    return ((k, k_oxs), (a, a_oxs))

def iSa_oxs(comp: 'Formula') -> ((str, int), (str, int)):
    salt = Compound(comp.value)

    me: str; me_oxs: int
    an: str; nme_oxs: int
    if salt.comp_type == "iSaNo" or salt.comp_type == "iSaAmm":
        ((me, me_oxs), (an, an_oxs)) =  _iSaNo_oxs(salt)
    elif salt.comp_type == "iSaAc" or salt.comp_type == "iSaAmmAc":
        ((me, me_oxs), (an, an_oxs)) = _iSaAc_oxs(salt)
    elif salt.comp_type == "iSaBa":
        ((me, me_oxs), (an, an_oxs)) = _iSaBa_oxs(salt)
    elif salt.comp_type == "iSaCo":
        ((me, me_oxs), (an, an_oxs)) = _iSaCo_oxs(salt)
    elif salt.comp_type == "iSaPer":
        s = Formula(salt.formula.value.replace("O2", "Cl"))
        ((me, me_oxs), _) = _iSaNo_oxs(salt)
        an, an_oxs = "O", 1
    else:
        ((me, me_oxs), (an, an_oxs)) =  _iSaNo_oxs(salt)

    if int(me_oxs) <= 0:
        me_oxs = 1
    if int(an_oxs) <= 0:
        an_oxs = 1
    return ((me, me_oxs), (an, an_oxs))

def iSaNo_create(kat, kat_oxs, an, an_oxs): # Kat{kat_q}An{an_q}
    mult = lcm(kat_oxs, an_oxs)
    kat_q = int(mult / kat_oxs)
    an_q = int(mult / an_oxs)

    if an_q > 1 and count_if(an, lambda c: c.isupper()) != 1 and an[0] != '[':
        an = "(" + an + ")"
    iSa = kat + index(kat_q) + an + index(an_q)
    return iSa

def iSaBa_create(kat, kat_oxs, an, an_oxs, oh_q=1): # Kat{kat_q}(OH){oh_q}An{an_q}
    mult = lcm(kat_oxs - oh_q, an_oxs)
    kat_q = int(mult / (kat_oxs - oh_q))
    an_q = int(mult / an_oxs)

    oh = "(OH)" + index(oh_q)

    if kat_q > 1:
        kat = "(" + kat + oh + ")"
    else:
        kat = kat + oh
    if an_q > 1 and count_if(an, lambda c: c.isupper()) != 1:
        an = "(" + an + ")"
    iSa = kat + index(kat_q) + an + index(an_q)
    return iSa

def iSaAc_create(kat, kat_oxs, an, an_oxs, h_q=1): #Kat{kat_q}H{h_q}An{an_q}
    mult = lcm(kat_oxs, an_oxs - h_q)
    kat_q = int(mult / kat_oxs)
    an_q = int(mult / (an_oxs - h_q))

    if an_q > 1:
        an = "(" + "H" + index(h_q) + an + ")"
    else:
        an = "H" + index(h_q) + an
    iSa = kat + index(kat_q) + an + index(an_q)
    return iSa

def iSaCo_create(k_cxs: (str, int, int), an_cxs: (str, int, int)) -> (str):
    is_up = lambda c: c.isupper()

    kat = ""
    kat_oxs = 0
    for k in k_cxs:
        if count_if(k[0], is_up) > 1:
            kat += "(" + k[0] + ")"
        else:
            kat += k[0]
        kat += index(k[2])
        kat_oxs += k[2] * k[1]
    if len(k_cxs) != 1:
        kat = "[" + kat + "]"

    an = ""
    an_oxs = 0
    for a in an_cxs:
        if count_if(a[0], is_up) > 1:
            an += "(" + a[0] + ")"
        else:
            an += a[0]
        an += index(a[2])
        an_oxs += a[2] * a[1]
    if len(an_cxs) != 1:
        an = "[" + an + "]"

    if kat_oxs == 0:
        kat_oxs = 1
    if an_oxs == 0:
        an_oxs = 1

    an_oxs = abs(an_oxs)
    mult = lcm(kat_oxs, an_oxs)
    kat_q = int(mult / kat_oxs)
    an_q = int(mult / an_oxs)

    iCo = kat + index(kat_q) + an + index(an_q)
    return iCo

def iSaCo_in(sph: str):
    is_up = lambda c: c.isupper() or c == "("

    # central atom
    me_end = find_if(sph[1 : ], is_up) + 1
    me = sph[0 : me_end]
    me_oxs = get_me_oxs(me)
    if me_oxs == 0:
        me_oxs == 1
    sph = sph.replace(me, "")

    # neutral molecules
    neu = ""
    neu_q = 0
    if "(H2O)" in sph:
        neu = "H2O"
    elif "(NH3)" in sph:
        neu = "NH3"
    sph = sph.replace(neu, "")

    if neu != "":
        neu_end = sph.find("()") + 2
        neu_qend = find_if(sph[neu_end], is_up)
        if neu_qend == -1:
            neu_qend = len(sph)
        else:
            neu_qend += neu_end

        neu_q = sph[neu_end : neu_qend]
        if neu_q == "":
            neu_q = 1
        else:
            neu_q = int(neu_q)
        sph = sph[0 : neu_end - 2] + sph[neu_qend : ]

    hoh = ""
    hoh_q = 0
    if "(OH)" in sph:
        hoh = "OH"
    elif "H" in sph:
        hoh = "H"
    sph = sph.replace("OH", "").replace("H", "()")

    if hoh != "":
        hoh_end = sph.find("()") + 2
        hoh_qend = find_if(sph[hoh_end], is_up)
        if hoh_qend == -1:
            hoh_qend = len(sph)
        else:
            hoh_qend += hoh_end

        hoh_q = sph[hoh_end : hoh_qend]
        if hoh_q == "":
            hoh_q = 1
        else:
            hoh_q = int(hoh_q)
        sph = sph[0 : hoh_end - 2] + sph[hoh_qend : ]

    # anions
    an = ""
    an_oxs = 0
    an_q = 0
    if len(sph) != 0 and sph[0] != '(':
        if count_if(sph, lambda c: c.isupper()) > 1:
            an = sph
            if an in db_anions:
                an_oxs = db_anions[an]
            else:
                an_oxs = 1
            an_q = 1
        else:
            an_end = find_if(sph, lambda c: c.isdigit())
            if an_end == -1:
                an_end = len(sph)
            an = sph[0 : an_end]

            if an in db_anions:
                an_oxs = db_anions[an]
            else:
                an_oxs = 1

            an_q = sph[an_end : ]
            if an_q == "":
                an_q = 1
            else:
                an_q = int(an_q)
    elif len(sph) != 0:
        an_end = sph.find(')')
        an = sph[1 : an_end]
        if an in db_anions:
            an_oxs = db_anions[an]
        else:
            an_oxs = 1
        an_q = sph[an_end + 1 :]
        if an_q == "":
            an_q = 1
        else:
            an_q = int(an_q)

    if an == "":
        an = None
    if hoh == "":
        hoh = None
    if neu == "":
        neu = None

    cxs = [(me, me_oxs, 1), (an, -an_oxs, an_q), (hoh, -1, hoh_q), (neu, 0, neu_q)]
    return cxs
