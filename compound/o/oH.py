from tools.comps import chain, index

def oHAa_parse(skel: 'Skeleton') -> (int):
    res = chain(skel.skeleton).count("C")
    return res

def oHAe_parse(skel: 'Skeleton') -> (int, int):
    ch = chain(skel.skeleton)
    res = ch.count("C")
    pos = int((ch.find("=")+1) / 2)
    return (res, pos)

def oHAy_parse(skel: 'Skeleton') -> (int, int):
    ch = chain(skel.skeleton)
    res = ch.count("C")
    pos = int((ch.find("#")+1) / 2)
    return (res, pos)

def oHDi_parse(skel: 'Skeleton') -> (int, int):
    ch = chain(skel.skeleton)
    res = ch.count("C")
    pos1 = int((ch.find("=")+1) / 2)
    pos2 = int((ch[pos1*2 : ].find("=") + pos1*2 + 1) / 2)
    return (res, (pos1, pos2))

def oHCa_parse(skel: 'Skeleton') -> (int):
    val = skel.skeleton
    obr = val.find("{-")
    cbr = val.find("-}")
    cycle = val[obr+2 : cbr]
    ch = chain(cycle)
    res = ch.count("C")
    return res

def oHAr_parse(skel: 'Skeleton') -> (int):
    res = skel.skeleton.count("C")
    return res

def oHAa_create(n: int) -> (str):
    if n == 1:
        return "CH4"
    res = "CH3-"
    for i in range(2, n):
        res += "CH2-"
    res += "CH3"
    return res

def oHAe_create(n: int, p=1) -> (str):
    if n == 2:
        return "CH2=CH2"

    res: str
    if p == 1:
        res = "CH2="
    else:
        res = "CH3-"

    for i in range(2, n):
        if i == p:
            res += "CH="
        else:
            if res[-1] == "=":
                res += "CH-"
            else:
                res += "CH2-"
        n -= 1

    if res[-1] == "=":
        res += "CH2"
    else:
        res += "CH3"
    return res

def oHAy_create(n: int, p=1) -> (str):
    if n == 2:
        return "CH#CH"

    res: str
    if p == 1:
        res = "CH#"
    else:
        res = "CH3-"

    for i in range(2, n):
        if i == p:
            res += "C#"
        else:
            if res[-1] == "#":
                res += "C-"
            else:
                res += "CH2-"
        n -= 1

    if res[-1] == "#":
        res += "CH"
    else:
        res += "CH3"
    return res

def oHDi_create(n: int, p=(1, 2)) -> (str):
    res: str
    if 1 in p:
        res = "CH2="
    else:
        res = "CH3-"

    for i in range(2, n):
        if i in p:
            if res[-1] == "=":
                res += "C="
            else:
                res += "CH="
        else:
            if res[-1] == "=":
                res += "CH-"
            else:
                res += "CH2-"

    if res[-1] == "=":
        res += "CH2"
    else:
        res += "CH3"
    return res

def oHCa_create(n: int):
    res = "{"
    for i in range(n):
        res += "-CH"
    res += "-}"
    return res

def oHAr_create(n: int) -> (str):
    res = "Bz"
    for i in range(min(n, 6)):
        res += "(-CH3)"
    if n < 6:
        res += "H" + index(6-n)

    sub = "(-"
    for i in range(6, n):
        sub += "CH2-"
    sub += "CH3)"

    res = res.replace("(-CH3)", sub, 1)
    return res
