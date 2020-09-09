import numpy as np

from compound import *
from database.compounds.gases import *
from database.compounds.solubility import *
from database.compounds.unstable import *
from element import Element
from formula import *
from tools.comps import index
from tools.math import gcd, rnd

# class for inreversable chemical reaction
class Reaction:
    value: str # string describing reaction
    bal_value: str
    cond: str # string containing condition of reaction's going
    inp: 'list(Compound)' # input compounds of reaction
    outp: 'list(Compound)' # output compounds of reaction
    coefs: 'dict(str, int)'

    # replace unstable compound to result of decomposition
    def unstable(self, comps, is_input):
        for c in comps:
            comp = str(c)
            if comp in db_unstable:
                prod = db_unstable[comp]
                del comps[comps.index(c)]
                comps += list(map(lambda c: Compound(c), prod))

                coef = self.coefs[c.formula.value]
                del self.coefs[c.formula.value]
                cs = ""
                for _p in prod:
                    p = Compound(_p)
                    self.coefs[_p] = coef
                    cs += index(coef) + repr(p)
                    if not is_input:
                        if is_gase(p):
                            cs += "↑"
                        elif not is_ionic_soluble(p):
                            cs += "↓"
                    cs += " + "
                cs = cs[:-3:]

                self.bal_value = \
                    self.bal_value.replace(index(coef) + repr(c), cs)
        return comps

    # separate reaction's string at list of compound
    def separate(self):
        r_in, r_out = self.value.split("->", 2)
        r_in = " ".join(r_in.split("+")) # list of compounds
        r_out = " ".join(r_out.split("+"))

        r_in = [str(Compound(c)) for c in r_in.split()] # erase spaces
        r_out = [str(Compound(c)) for c in r_out.split()]

        r_in = sorted(set(r_in))
        r_out = sorted(set(r_out))

        r_input = list(map(lambda c: Compound(c), r_in))
        r_output = list(map(lambda c: Compound(c), r_out))

        self.value = " + ".join(r_in) + " -> " + " + ".join(r_out)
        return (r_input, r_output)

    def equ(self):
        r_in = set(map(lambda c: c.formula.value, self.inp))
        r_out = set(map(lambda c: c.formula.value, self.outp))
        return r_in == r_out

    def balance(self):
        comps = self.inp + self.outp
        elems = []
        for comp in comps:
            for el in comp.formula.consist:
                if el.name == "Amm":
                    elems.append(Element("N"))
                    elems.append(Element("H"))
                else:
                    elems.append(el)

        bz = False
        if Element("Bz") in elems:
            del elems[elems.index(Element("Bz"))]
            elems.append(Element("C"))
            bz = True
        elems = list(set(elems))

        rows = []
        for i in elems:
            rows.append([])

        for comp in self.inp:
            for i in range(len(elems)):
                val = 0
                if Element("Amm") in comp.formula.consist:
                    if elems[i].name == "H":
                        val += comp.formula.consist[Element("Amm")] * 4
                    elif elems[i].name == "N":
                        val += comp.formula.consist[Element("Amm")]
                if Element("Bz") in comp.formula.consist:
                    if elems[i].name == "C":
                        val += comp.formula.consist[Element("Bz")] * 6
                if elems[i] in comp.formula.consist:
                    val += comp.formula.consist[elems[i]]
                rows[i].append(val)
        for comp in self.outp:
            for i in range(len(elems)):
                val = 0
                if Element("Amm") in comp.formula.consist:
                    if elems[i].name == "H":
                        val += comp.formula.consist[Element("Amm")] * 4
                    elif elems[i].name == "N":
                        val += comp.formula.consist[Element("Amm")]
                if Element("Bz") in comp.formula.consist:
                    if elems[i].name == "C":
                        val += comp.formula.consist[Element("Bz")] * 6
                if elems[i] in comp.formula.consist:
                    val += comp.formula.consist[elems[i]]
                rows[i].append(-val)

        while len(rows[0]) > len(rows):
            rows.append([0] * len(comps))

        free = [r.pop(-1) for r in rows]

        while len(rows) > len(rows[0]):
            for i in range(len(rows)):
                rows[i].append(0)

        (coefs, _, _, _) = np.linalg.lstsq(np.array(rows), np.array(free), rcond=None)
        coefs = coefs.tolist()
        coefs = [abs(c) for c in coefs if c != 0]

        m = min(coefs)
        coefs = list(map(lambda c: round(rnd((c / m) * 2520)), coefs))
        coefs.append(round(rnd((1 / m) * 2520)))

        div = coefs[0]
        for c in coefs:
            div = gcd(c, div)

        coefs = list(map(lambda c: int(round(c) / div), coefs))

        val = ""
        for i in range(len(self.inp)):
            val += index(coefs[i])
            val += repr(self.inp[i])
            val += " + "
        val = val[0 : -2]
        val += "→ "
        for i in range(len(self.outp)):
            val += index(coefs[len(self.inp) + i])
            val += repr(self.outp[i])
            if is_gase(self.outp[i]):
                val += "↑"
            elif not is_ionic_soluble(self.outp[i]):
                val += "↓"
            val += " + "
        val = val[0 : -2]

        self.coefs = dict(zip(map(lambda c: c.formula.value, comps), coefs))
        return val

    def count_mass(self, c: str, mass: float):
        comp = Compound(c)
        mult = mass / (comp.formula.molar * self.coefs[comp.formula.value])
        ms = []
        for x in (self.inp + self.outp):
            i = mult * self.coefs[x.formula.value] * x.formula.molar
            ms.append(round(i * 100) / 100)
        return ms

    def load_cond(self, cond):
        cond = cond.replace("t ", "; нагревание").replace("p ", "; давление").\
             replace("te- ", "; расплав, эл. ток").replace("e- ", "; эл. ток").\
             replace("hv ", "; свет").replace("c: ", "; катализатор: ").\
             replace("c ", "; катализатор ")
        return cond

    def __str__(self):
        str_val = self.bal_value
        return str_val + self.cond

    # constructor
    def __init__(self, value, cond = ""):
        self.value = value
        self.cond = self.load_cond(cond)
        (self.inp, self.outp) = self.separate()

        if self.equ():
            self.value = ""
            self.cond = ""
            return

        self.bal_value = self.balance()
        (self.inp, self.outp) = (self.unstable(self.inp, True),\
                                 self.unstable(self.outp, False))

        if self.equ():
            self.value = ""
            self.cond = ""

