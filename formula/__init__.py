from database.elements.weights import *
from element import Element
from tools.container import find_if

# formula of chemical compound with its consist
class Formula:
    value: str # string describing formula
    ext_value: str # formula with 1-indices and without brackets
    consist: 'dict(Element, int)' # quantity of atoms of every elements in compound

    # replace square brackets to round
    def replace_brackets(self, value):
        new_value = value.replace('[', '(').replace(']', ')')
        return new_value

    # add index 1 where it is omitted
    def add1(self, value):
        iter_value = value
        new_value = ""

        while iter_value:
            is_up = lambda c: c.isupper() or (c in "()")
            up_pos = find_if(iter_value[1 : ], is_up) + 1
            sub_str = ""

            if up_pos == 0:
                sub_str = iter_value
            else:
                sub_str = iter_value[0 : up_pos]

            if not sub_str[-1].isdigit() and sub_str[-1] != '(':
                sub_str += "1"
            new_value += sub_str

            if up_pos == 0:
                break
            iter_value = iter_value[up_pos : ]

        return new_value

    # change formula's view, deleting brackets
    def open_brackets(self, value):
        iter_value = value
        new_value = ""

        while iter_value:
            par_pos = iter_value.find('(')
            bef_par, par_value = iter_value[0 : par_pos], iter_value[par_pos : ]

            if par_pos == -1:
                new_value += iter_value
                break
            brackets = 0
            par_end = 0

            for i in range(len(par_value)):
                if par_value[i] == '(':
                    brackets += 1
                elif par_value[i] == ')':
                    brackets -= 1
                if brackets == 0:
                    par_end = i
                    break

            num_value = par_value[par_end + 1 : ]
            par_value = par_value[0 : par_end + 1]
            num_end = -1

            for i in range(len(num_value)):
                if num_value[i].isdigit():
                    num_end += 1
                else:
                    break

            iter_value = num_value[num_end + 1 : ]
            num_value = num_value[0 : num_end + 1]
            have_par = find_if(par_value[1 : -1], lambda c: c in "()")

            if have_par != -1:
                par_value = "(" + self.open_brackets(par_value[1 : -1]) + ")"

            new_par_value = self.multiply(par_value, num_value)
            new_value += bef_par + new_par_value

        return new_value

    # get the part of formula and multiplier;
    # multiply every number in formula by multiplier
    def multiply(self, par: str, mult: str):
        iter_value = par[1 : -1]
        new_value = ""

        while iter_value:
            num_pos = find_if(iter_value, lambda c: c.isdigit())
            bef_num, num_value = iter_value[0 : num_pos], iter_value[num_pos : ]
            num_end = -1

            for i in range(len(num_value)):
                if num_value[i].isdigit():
                    num_end += 1
                else:
                    break

            if num_end == len(num_value):
                num_value = str(int(num_value))
                new_value += bef_num + num_value
                break

            iter_value = num_value[num_end + 1 : ]
            num_value = num_value[0 : num_end + 1]
            num_value = str(int(num_value) * int(mult))
            new_value += bef_num + num_value

        return new_value

    # create the dictionary describing consist of formula
    def separate(self):
        iter_value = self.ext_value
        new_consist = dict()

        while iter_value:
            up_pos = find_if(iter_value[1 : ], lambda c: c.isupper()) + 1
            sub_str = iter_value[0 : up_pos]
            if up_pos == 0:
                sub_str = iter_value

            num_pos = find_if(sub_str, lambda c: c.isdigit())
            el_value = sub_str[0 : num_pos]
            num_value = int(sub_str[num_pos : ])

            element = Element(el_value)
            new_consist[element] = new_consist.get(element, 0) + num_value

            if up_pos == 0:
                break
            iter_value = iter_value[up_pos : ]

        return new_consist

    def count_molar(self):
        mol = 0
        for el in self.consist:
            if el.name in db_weights:
                mol += self.consist[el] * db_weights[el.name]
        return mol

    # constructor
    def __init__(self, value):
        self.value = value
        self.ext_value =  self.open_brackets(self.add1(self.replace_brackets(
          value)))
        self.consist = self.separate()
        self.molar = self.count_molar()
