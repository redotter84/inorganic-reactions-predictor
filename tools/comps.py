from database.elements.elements import db_Hal
from database.organic.fun import *

def chain(skel):
    chain = ""
    br = 0
    for i in skel:
        if i == '(':
            br += 1
        elif i == ')':
            br -= 1
        elif br == 0:
            chain += i
    return chain

def coord(el, oxs):
    if oxs == 1:
        return (2, 2)
    elif oxs == 2:
        return (4, 6)
    elif oxs == 3:
        return (6, 4)
    elif oxs == 4:
        return (6, 8)
    elif oxs == 5:
        return (6, 6)
    else:
        return (oxs * 2, oxs * 2)

def index(x_quant: int) -> (str):
    if x_quant == 1:
        return ""
    else:
        return str(x_quant)

def simple(comp: str):
    if comp in ["H", "N", "O", "F", "Cl", "Br", "I"]:
        return comp + "2"
    else:
        return comp

def do_subst(skel: 'Skeleton', subst: 'list(tuple(int, str))') -> (str):
    val = skel.open_value

    for (p, s) in subst:
        val = val.replace("Cl", "cl")
        c_pos = val.replace("C", "&", p-1).find("C")
        c_end = val.replace("C", "&", p).find("C")
        if c_end == -1:
            c_end = len(val)
        val = val.replace("cl", "Cl")
        for i in db_fun_group1:
            val = val.replace(i, i.lower())

        oxs = 1
        if s in db_fun_group1:
            oxs = db_fun_group1[s]
            s = f"({s})"
        elif s in db_fun_group2:
            oxs = db_fun_group2[s]
        elif s in db_fun_group3:
            oxs = db_fun_group3[s]

        repl = val[c_pos : c_end][::-1].replace("H"*oxs, s[::-1], 1)[::-1]
        val = val[0 : c_pos] + repl + val[c_end : ]

        for i in db_fun_group1:
            val = val.replace(i.lower(), i)

    h = 0

    for h in ["H"] + list(db_Hal):
        for i in range(4, 1, -1):
            val = val.replace(h*i, f"{h}{i}")

    return val
