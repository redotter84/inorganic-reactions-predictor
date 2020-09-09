from tools.comps import chain, do_subst
from tools.container import flatten

def oOAlc_parse(skel: 'Skeleton') -> (int, 'list(int)'):
    c = chain(skel.skeleton).count("C")
    subst = flatten(skel.subst)
    ohs = []
    for i in range(len(subst)):
        if subst[i] == "OH":
            ohs += [int(i/4) + 1]
    return (c, ohs)

def oOAc_parse(skel: 'Skeleton') -> (int, 'list(int)'):
    c = chain(skel.skeleton).count("C")
    subst = flatten(skel.subst)
    cs = []
    for i in range(len(subst)):
        if subst[i] == "O" and subst[i+1] == "OH":
            cs += [int(i/4) + 1]
    return (c, cs)

def oOAld_parse(skel: 'Skeleton') -> (int):
    res = chain(skel.skeleton).count("C")
    return res

def oOKet_parse(skel: 'Skeleton') -> (int, int):
    c = chain(skel.skeleton).count("C")
    subst = flatten(skel.subst)
    os = []
    for i in range(len(subst)):
        if subst[i] == "O":
            os += [int(i/4) + 1]
    return (c, os)

def oOEth_parse(skel: 'Skeleton') -> (int, int):
    val = skel.value
    o = val.find("-O-")
    a1 = val[0 : o]
    a2 = val[o+3 : ]
    c1 = a1.count("C")
    c2 = a2.count("C")
    return (c1, c2)

def oOAlc_create(alk: 'Skeleton', oh_p=[]) -> (str):
    if oh_p == []:
        oh_p = [chain(alk.skeleton).count("C")]
    subst = [(x, "OH") for x in oh_p]
    res = do_subst(alk, subst)
    return res

def oOAc_create(alk: 'Skeleton', cooh_p=[]):
    if cooh_p == []:
        cooh_p = [chain(alk.skeleton).count("C")]
    subst = flatten([[(x, "OH"), (x, "O")] for x in cooh_p])
    res = do_subst(alk, subst)
    return res

def oOAld_create(alk: 'Skeleton') -> (str):
    c = chain(alk.skeleton).count("C")
    res = do_subst(alk, [(c, "HO")])
    return res

def oOKet_create(alk: 'Skeleton', o_p=2) -> (str):
    res = do_subst(alk, [(o_p, "O")])
    return res

def oOEth_create(alk1: 'Skeleton', alk2: 'Skeleton') -> (str):
    c1 = chain(alk1.skeleton).count("C")
    a1 = do_subst(alk1, [(c1, "")])
    a2 = do_subst(alk2, [(1, "")])
    res = a1 + "-O-" + a2
    return res
