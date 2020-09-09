# great common divisor
def gcd(a: int, b: int) -> (int):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

# less common multiple
def lcm(a: int, b: int) -> (int):
    return (a * b) / gcd(a, b)

def rnd(i):
    if 10 * (i - int(i)) >= 9 or \
       10 * (i - int(i)) <= 1:
       return round(i)
    elif 10 * (i - int(i)) >= 3.3 and \
         10 * (i - int(i)) <= 6.7:
       return int(i) + 0.5
    else:
        return i
