from compound import Compound
from database.compounds.unstable import db_unstable
from database.reacts import *
from reaction import Reaction
from tools.container import find_if

import reacts.inorganic
import reacts.organic

# load functions r_{#} from modules r{#}-r{#}
def load_functs():
    rs = inorganic.load_functs()
    i = 0
    for r in rs:
        i = i + 1
        yield r
    rs = organic.load_functs()
    for r in rs:
        i = i + 1
        yield r

# select and calculate reactions for compound
def reacts(cs: 'list(str)', is_input):
    functs = load_functs()
    cs = sorted(set(cs))
    comps = list(map(lambda c: Compound(c), cs))

    for (x, cond) in db_reacts:
        (r_input, r_output) = x.split("->", 2)
        if is_input:
            react = True
            for c in comps:
                val: str
                if c.comp_type[0] == "o":
                    val = c.skeleton.value
                else:
                    val = c.formula.value

                if f"`{val}`" not in r_input:
                    react = False
                    break
                else:
                    r_input = r_input.replace(f"`{val}`", "", 1)
        else:
            react = True
            for c in comps:
                val: str
                if c.comp_type[0] == "o":
                    val = c.skeleton.value
                else:
                    val = c.formula.value

                if f"`{val}`" not in r_output:
                    react = False
                    break
                else:
                    r_output = r_output.replace(f"`{val}`", "", 1)
        if not react:
            continue
        r = Reaction(x.replace("`", ""), cond)
        yield r

    comp_types = set([
        "iOxAlk", "iOxBa", "iOxAm", "iOxAc", "iOxNs",
        "iBaAlk", "iBaBa", "iBaAm", "iBaCo"
        "iAcNox", "iAcOx", "iAcCo",
        "iSaNo", "iSaAc", "iSaBa",
        "iSaAmm", "iSaAmac", "iSaCo", "iSaPer",
        "iSiMe", "iSiNme", "iBi", "iWa",
        "oH*", "oHAa", "oHAe", "oHAy", "oHDi", "oHCa", "oHAr",
        "oO*", "oOAc", "oOAlc", "oOEth", "oOAld", "oOKet",
        "oN*", "oNAc", "oNAm", "oNNi",
        "oBioHy", "oBioLi",
        "oHal", "oP*", "oS*", "oHe*",
        "nil"
    ])
    is_space = lambda c: c in " ,)"
    for f in functs:
        (r_input, r_output) = f.__doc__.split("->", 2) # analyse documentation string
        if is_input:
            react = True
            for c in comps:
                c_t = c.comp_type
                val: str
                if c_t[0] == "o":
                    val = c.skeleton.value
                else:
                    val = c.formula.value

                if f"`{val}`" not in r_input: # formula
                    if f"`{c_t}" not in r_input: # type
                        react = False
                        break
                    else:
                        if f"`{c_t}_" in r_input:
                            temp = r_input
                            type_str = temp.find(f"`{c_t}")
                            temp = temp.replace(f"`{c_t}", "", 1)
                            sp_str = find_if(temp[type_str : ], is_space)
                            sp_q = sp_str
                            sp = "_" * sp_q
                            for i in comp_types:
                                r_input = r_input.replace(f"`{i}{sp},", "")
                                r_input = r_input.replace(f"`{i}{sp})", "")
                            for i in comps:
                                v = i.formula.value
                                r_input = r_input.replace(f"`{v}`{sp},", "")
                                r_input = r_input.replace(f"`{v}`{sp})", "")
                        else:
                            r_input = r_input.replace(f"`{c_t}", "", 1)
                else:
                    if True:
                        if f"`{val}`_" in r_input:
                            temp = r_input
                            type_str = temp.find(f"`{val}`")
                            temp = temp.replace(f"`{val}`", "", 1)
                            sp_str = find_if(temp[type_str : ], is_space)
                            sp_q = sp_str
                            sp = "_" * sp_q
                            for i in comp_types:
                                r_input = r_input.replace(f"`{i}{sp},", "")
                                r_input = r_input.replace(f"`{i}{sp})", "")
                            for i in comps:
                                v = i.formula.value
                                r_input = r_input.replace(f"`{v}`{sp},", "")
                                r_input = r_input.replace(f"`{v}`{sp})", "")
                        else:
                            r_input = r_input.replace(f"`{val}`", "", 1)
        else:
            react = True
            for c in comps:
                c_t = c.comp_type
                val: str
                if c_t[0] == "o":
                    val = c.skeleton.value
                else:
                    val = c.formula.value

                if f"`{val}`" not in r_output: # formula
                    if f"`{c_t}" not in r_output: # type
                        react = False
                        break
                    else:
                        if f"`{c_t}_" in r_output:
                            temp = r_output
                            type_str = temp.find(f"`{c_t}")
                            temp = temp.replace(f"`{c_t}", "", 1)
                            sp_str = find_if(temp[type_str : ], is_space)
                            sp_q = sp_str
                            sp = "_" * sp_q
                            for i in comp_types:
                                r_output = r_output.replace(f"`{i}{sp},", "")
                                r_output = r_output.replace(f"`{i}{sp})", "")
                            for i in comps:
                                v = i.formula.value
                                r_output = r_output.replace(f"`{v}`{sp},", "")
                                r_output = r_output.replace(f"`{v}`{sp})", "")
                        else:
                            r_output = r_output.replace(f"`{c_t}", "", 1)
                else:
                    if True:
                        if f"`{val}`_" in r_output:
                            temp = r_output
                            type_str = temp.find(f"`{val}`")
                            temp = temp.replace(f"`{val}`", "", 1)
                            sp_str = find_if(temp[type_str : ], is_space)
                            sp_q = sp_str
                            sp = "_" * sp_q
                            for i in comp_types:
                                r_output = r_output.replace(f"`{i}{sp},", "")
                                r_output = r_output.replace(f"`{i}{sp})", "")
                            for i in comps:
                                v = i.formula.value
                                r_output = r_output.replace(f"`{v}`{sp},", "")
                                r_output = r_output.replace(f"`{v}`{sp})", "")
                        else:
                            r_output = r_output.replace(f"`{val}`", "", 1)

        if not react:
            continue
        r = f(comps, is_input)
        if type(r) == list:
            for i in r:
                if i != "" and i.value != "":
                    yield i
        elif r != "" and r.value != "":
            yield r

    for c in comps:
        for uns, prod in db_unstable.items():
            if c.formula.value in prod:
                _cs = [x for x in cs if x != c.formula.value]
                _cs.append(uns)
                rs = reacts(_cs, is_input)
                for r in rs:
                    yield r
