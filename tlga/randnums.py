# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import ones
from numpy.random import seed, random, randint, shuffle

def Seed(val):
    """
    Seed initialises random numbers generator
    """
    seed(val)


def IntRand(low, high=None, size=None):
    """
    IntRand generates random integers
    """
    return randint(low, high, size)


def FltRand(n, xa=0.0, xb=1.0):
    """
    FltRand generates n numbers between xa and xb
    """
    return random(n) * (xb - xa) + xa


def FlipCoin(p):
    """
    Flip generates a Bernoulli variable; throw a coin with probability p
    """
    if p==1.0: return True
    if p==0.0: return False
    if random()<=p: return True
    return False


def Shuffle(x):
    """
    Shuffle modifies an array by shuffling its contents
    """
    shuffle(x)


if __name__ == "__main__":
    from numpy import array
    a = array([1,2,3,4,5], dtype=int)
    print 'before: a =', a
    Shuffle(a)
    print 'after:  a =', a
