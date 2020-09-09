from tools.comps import chain, do_subst
from tools.container import flatten

def oNNi_parse(skel: 'Skeleton') -> (int, 'list(int)'):
    c = chain(skel.skeleton).count("C")
    subst = flatten(skel.subst)
    ohs = []
    for i in range(len(subst)):
        if subst[i] == "NOO":
            ohs += [int(i/4) + 1]
    return (c, ohs)

def oNNi_create(alk: 'Skeleton', no2_p=[]) -> (str):
    if no2_p == []:
        no2_p = [chain(alk.skeleton).count("C")]
    subst = [(x, "NO2") for x in no2_p]
    res = do_subst(alk, subst)
    return res
