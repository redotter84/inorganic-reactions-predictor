from database.elements.elements import db_Hal
from tools.comps import chain, do_subst
from tools.container import flatten

def oHal_parse(skel: 'Skeleton') -> (int, 'list(tuple(int, str))'):
    c = chain(skel.skeleton).count("C")
    subst = flatten(skel.subst)
    hals = []
    for i in range(len(subst)):
        if subst[i] in db_Hal:
            hals += [(int(i/4) + 1, subst[i])]
    return (c, hals)

def oHal_create(alk: 'Skeleton', hal: 'list(tuple(int, str))', hal_p=[]) -> (int):
    if hal_p == []:
        hal_p = [4] * len(hal)
    sk = alk
    subst = []
    for i in range(len(hal_p)):
        subst += [hal[i]] * hal_p[i]
    res = do_subst(alk, subst)
    return res
