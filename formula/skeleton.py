from database.organic.fun import *
from database.elements.oxs import *

class Skeleton:
    value: str
    open_value: str
    skeleton: str
    subst: 'list'

    def open_index(self, val):
        for i in range(2, 9):
            for f in db_fun_group1:
                val = val.replace(f"({f}){i}", f"({f})" * i)
            for f in db_fun_group2:
                val = val.replace(f"{f}{i}", f * i)
            for f in db_fun_group3:
                val = val.replace(f"{f}{i}", f * i)
        return val

    def find_br(self, val, pos):
        br = 1
        while br != 0 and pos < len(val):
            if val[pos] == '(':
                br += 1
            elif val[pos] == ')':
                br -= 1
            pos += 1
        return pos

    def skel(self, val, br=False):
        skel: str = ""
        skel_subst = [[]]
        c_bind = 0
        pos = 0
        cur = -1

        while pos < len(val):
            if pos == 0 and not br:
                el = ""
                if pos != len(val)-1 and val[0 : 2] in db_oxs:
                    el = val[0 : 2]
                elif val[0] in db_oxs:
                    el = val[0]

                if el != "":
                    cur = 0
                    c_bind += abs(min(db_oxs[el]))
                    skel += el
                else:
                    skel += val[pos]

            elif val in db_fun_group1:
                skel_subst[cur] += [val]
                c = db_fun_group1[val]
                if c_bind == c - 1:
                    skel_subst += [[]]
                break

            elif val[pos : pos+2] in db_fun_group2:
                skel_subst[cur] += [val[pos : pos+2]]
                c = db_fun_group2[val[pos : pos+2]]
                if c_bind == c - 1:
                    skel += val[pos : pos+2]
                    cur += 1
                    skel_subst += [[]]
                    pos += 2
                c_bind -= c

            elif val[pos] in db_fun_group3:
                skel_subst[cur] += [val[pos]]
                c = db_fun_group3[val[pos]]
                if c_bind == c - 1:
                    skel += val[pos]
                    cur += 1
                    skel_subst += [[]]
                    pos += 1
                c_bind -= c

            elif val[pos] == "(":
                end_pos = self.find_br(val, pos+1)
                sub = Skeleton(val[pos+1 : end_pos-1], br=True)

                if sub.skeleton != "":
                    skel += "(" + sub.skeleton + ")"
                    skel_subst[cur] += [sub.subst]
                else:
                    for s in sub.subst:
                        skel_subst[cur] += s

                if val[pos+1] == "-":
                    c_bind -= 1
                elif val[pos+1] == "=":
                    c_bind -= 2
                elif val[pos+1] == "#":
                    c_bind -= 3
                pos = end_pos - 1

            elif val[pos] in "(-(=(#":
                if val[pos] in "(-":
                    skel += "-"
                    c_bind -= 1
                elif val[pos] in "(=":
                    skel += "="
                    c_bind -= 2
                elif val[pos] in "(#":
                    skel += "#"
                    c_bind -= 3

                el = ""
                if pos != len(val)-1 and val[pos+1 : pos+3] in db_oxs:
                    el = val[pos+1 : pos+3]
                elif val[pos+1] in db_oxs:
                    el = val[pos+1]

                if el != "":
                    c_bind += abs(min(db_oxs[el]))
                    skel += el
                    cur += 1
                    skel_subst += [[]]
                    pos += 1

            elif val[pos] in "{}":
                skel += val[pos]

            pos += 1

        return skel, skel_subst

    def change_val(self, val):
        op_val = val
        for fun in db_fun_group1:
            if op_val != fun:
                op_val = op_val.replace(f"({fun})", "fbr").replace(f"{fun}", "fbr").\
                   replace("fbr", f"({fun})")

        return op_val

    def __init__(self, val, br=False):
        self.value = val
        if self.value == "H4C":
            self.value = "CH4"

        self.open_value = self.open_index(self.change_val(self.value))
        (self.skeleton, self.subst) = self.skel(self.open_value, br)
        if self.value[0] in "-=#":
            self.subst = self.subst[0 : -1]

        if self.value not in db_fun_group1:
            for i in range(len(self.subst)):
                while len(self.subst[i]) < 4:
                    self.subst[i] = [0] + self.subst[i]
