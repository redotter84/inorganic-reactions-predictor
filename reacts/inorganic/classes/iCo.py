from compound import *
from compound.i.iOx import *
from compound.i.iBa import *
from compound.i.iSa import *
from element import get_me_oxs
from reaction import *
from tools.comps import coord, simple

def r_1(comps: 'list(Compound)', is_input):
    """`iBaAlk + `iBaAm -> `iSaCo"""
    react: str

    if is_input:
        iBaAlk = Compound("NaOH")
        iBaAm = Compound("Zn(OH)2")
        if len(comps) == 1:
            if "iBaAlk" in comps[0].comp_type:
                iBaAlk = comps[0]
            else:
                iBaAm = comps[0]
        else:
            if "iBaAlk" in comps[0].comp_type:
                iBaAlk = comps[0]
                iBaAm = comps[1]
            else:
                iBaAlk = comps[1]
                iBaAm = comps[0]

        (me, me_oxs) = iBa_oxs(iBaAlk.formula)
        (ame, ame_oxs) = iBa_oxs(iBaAm.formula)
        coo = coord(ame, ame_oxs)[0]
        if ame == "Al":
            coo = 4

        kat = [(me, me_oxs, 1)]
        an = [(ame, ame_oxs, 1), ("OH", -1, coo)]
        iSaCo = Compound(iSaCo_create(kat, an))

        react = f"{iBaAlk} + {iBaAm} -> {iSaCo}"
    else:
        iSaCo = comps[0]

        ((me, me_oxs), (cpx, _)) = iSa_oxs(iSaCo.formula)
        [(ame, ame_oxs, _), an, oh, neu] = iSaCo_in(cpx[1:-1])
        if oh[0] != "OH" or an[0] != None or neu[0] != None:
            return ""

        iBaAlk = Compound(iBa_create(me, me_oxs))
        iBaAm = Compound(iBa_create(ame, ame_oxs))

        react = f"{iBaAlk} + {iBaAm} -> {iSaCo}"

    return Reaction(react)

def r_2(comps: 'list(Compound)', is_input):
    """`iBaAlk + `iOxAm + `iWa -> `iSaCo"""
    react: str

    if is_input:
        iBaAlk = Compound("NaOH")
        iOxAm = Compound("ZnO")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
            elif "iOx" in comps[0].comp_type:
                iOxAm = comps[0]
        elif len(comps) == 2:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
            elif "iBa" in comps[1].comp_type:
                iBaAlk = comps[1]
            if "iOx" in comps[0].comp_type:
                iOxAm = comps[0]
            elif "iOx" in comps[1].comp_type:
                iOxAm = comps[1]
        else:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
                if "iOx" in comps[1].comp_type:
                    iOxAm = comps[1]
                else:
                    iOxAm = comps[2]
            elif "iBa" in comps[1].comp_type:
                iBaAlk = comps[1]
                if "iOx" in comps[0].comp_type:
                    iOxAm = comps[0]
                else:
                    iOxAm = comps[2]
            else:
                iBaAlk = comps[2]
                if "iOx" in comps[0].comp_type:
                    iOxAm = comps[0]
                else:
                    iOxAm = comps[1]

        (me, me_oxs) = iBa_oxs(iBaAlk.formula)
        (ame, ame_oxs) = iOx_oxs(iOxAm.formula)
        coo = coord(ame, ame_oxs)[0]
        if ame == "Al":
            coo = 4

        kat = [(me, me_oxs, 1)]
        an = [(ame, ame_oxs, 1), ("OH", -1, coo)]

        iSaCo = Compound(iSaCo_create(kat, an))

        react = f"{iBaAlk} + {iOxAm} + H2O -> {iSaCo}"
    else:
        iSaCo = comps[0]

        ((me, me_oxs), (cpx, _)) = iSa_oxs(iSaCo.formula)
        [(ame, ame_oxs, _), an, oh, neu] = iSaCo_in(cpx[1:-1])
        if oh[0] != "OH" or an[0] != None or neu[0] != None:
            return ""

        iBaAlk = Compound(iBa_create(me, me_oxs))
        iOxAm = Compound(iOx_create(ame, ame_oxs))
        if iOxAm.comp_type != "iOxAm":
            return ""

        react = f"{iBaAlk} + {iOxAm} + H2O -> {iSaCo}"

    return Reaction(react)

def r_3(comps: 'list(Compound)', is_input):
    """`iBaAlk + `iSiMe + `iWa -> `iSaCo + `H2`"""
    react: str

    if is_input:
        iBaAlk = Compound("NaOH")
        iSiMe = Compound("Al")
        if len(comps) == 1:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
            elif "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
        elif len(comps) == 2:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
            elif "iBa" in comps[1].comp_type:
                iBaAlk = comps[1]
            if "iSi" in comps[0].comp_type:
                iSiMe = comps[0]
            elif "iSi" in comps[1].comp_type:
                iSiMe = comps[1]
        else:
            if "iBa" in comps[0].comp_type:
                iBaAlk = comps[0]
                if "iSi" in comps[1].comp_type:
                    iSiMe = comps[1]
                else:
                    iSiMe = comps[2]
            elif "iBa" in comps[1].comp_type:
                iBaAlk = comps[1]
                if "iSi" in comps[0].comp_type:
                    iSiMe = comps[0]
                else:
                    iSiMe = comps[2]
            else:
                iBaAlk = comps[2]
                if "iSi" in comps[0].comp_type:
                    iSiMe = comps[0]
                else:
                    iSiMe = comps[1]

        (me, me_oxs) = iBa_oxs(iBaAlk.formula)
        ame = list(iSiMe.formula.consist.keys())[0].name
        ame_oxs = get_me_oxs(ame)
        if ame_oxs == 0:
            return ""
        iOxAm = Compound(iOx_create(ame, ame_oxs))
        if iOxAm.comp_type != "iOxAm":
            return ""

        coo = coord(ame, ame_oxs)[0]
        if ame == "Al":
            coo = 4

        kat = [(me, me_oxs, 1)]
        an = [(ame, ame_oxs, 1), ("OH", -1, coo)]

        iSaCo = Compound(iSaCo_create(kat, an))

        react = f"{iBaAlk} + {iSiMe} + H2O -> {iSaCo} + H2"
    else:
        iSaCo = Compound("Na[Al(OH)4]")
        if len(comps) == 1:
            if "iSa" in comps[0].comp_type:
                iSaCo = comps[0]
        else:
            if "iSa" in comps[0].comp_type:
                iSaCo = comps[0]
            else:
                iSaCo = comps[1]

        ((me, me_oxs), (cpx, _)) = iSa_oxs(iSaCo.formula)
        [(ame, ame_oxs, _), an, oh, neu] = iSaCo_in(cpx[1:-1])
        if oh[0] != "OH" or an[0] != None or neu[0] != None:
            return ""
        iOxAm = Compound(iOx_create(ame, ame_oxs))
        if iOxAm.comp_type != "iOxAm":
            return ""

        iBaAlk = Compound(iBa_create(me, me_oxs))
        iSiMe = Compound(simple(ame))

        react = f"{iBaAlk} + {iSiMe} + H2O -> {iSaCo} + H2"

    return Reaction(react)
