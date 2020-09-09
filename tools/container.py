# check if predicate returns True in enumerations (string, list, etc.)
# if does, return position where it is done; else return -1
def find_if(cont: 'list(any)', fn: 'function') -> (int):
    for i in range(len(cont)):
        if fn(cont[i]):
            return i
    return -1

# quantity of elements in enumerations for which predicate returns True
def count_if(cont: 'list(any)', fn: 'function') -> (int):
    res = 0
    for i in range(len(cont)):
        if fn(cont[i]):
            res = res + 1
    return res

# do smth similar to find_if, only for dictionary' keys
def key_in_dict(cont: 'list(any)', fn: 'function') -> (int):
    i = 0
    for x in cont.keys():
        if (fn(x)):
            i += 1
    return i

def flatten(l: 'list') -> ('list'):
    res = []
    for i in l:
        if type(i) == list:
            res += flatten(i)
        else:
            res += [i]
    return res
