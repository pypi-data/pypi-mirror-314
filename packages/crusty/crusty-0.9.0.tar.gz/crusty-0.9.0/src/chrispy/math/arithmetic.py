

def addition(augend, addend):

    sum                     = augend + addend

    return sum


def difference(minuend, subtrahend):

    diff                    = minuend - subtrahend 

    return diff


def multiplication(multiplier, multiplicand):

    product                 = multiplier * multiplicand

    return product


def division(numerator, denominator):
    
    quotient                = numerator / denominator

    return quotient


def nth_root(radicand, degree):

    root                    = radicand ** (division(1, degree))

    return root


def exponentiation(base, exponent):

    power                   = base ** exponent

    return power


def logarithm(logx, base):

    from math import log

    logarithm               = log(logx, base)

    return logarithm