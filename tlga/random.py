# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import ones
from numpy.random import seed, random, randint

def Seed(val):
    """
    Seed initialises random numbers generator
    """
    seed(val)


def RandInt(low, high=None, size=None):
    """
    RandInt generates random integers
    """
    return randint(low, high, size)


def Random(n, xa=0.0, xb=1.0):
    """
    Random generates n numbers between xa and xb
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
