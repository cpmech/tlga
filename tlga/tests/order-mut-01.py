# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import array

from tlga.random    import Seed
from tlga.operators import OrdMutation

from testing import CheckVector

# initialise random numbers generator
#Seed(1234) # use a fixed seed, so every time we run this code we will get the same results

# example 1 -----------------------------------------------------------------------------
print 'example 1 -----------------------------------------------------------------------------'

c = array([1,2,3,4,5,6,7,8], dtype=int)

print
print 'before: c =', c

c = OrdMutation(c, pm=1, cut1=2, cut2=5, ins=3)

print 'after:  c =', c
print

CheckVector('c', 'c_sol', c, [1,2,6,7,3,4,5,8])

c.sort()
CheckVector('sort(c)', '12345678', c, [1,2,3,4,5,6,7,8])

# example 2 -----------------------------------------------------------------------------
print 'example 2 -----------------------------------------------------------------------------'

c = array([1,2,3,4,5,6,7,8], dtype=int)

print
print 'before: c =', c

c = OrdMutation(c, pm=1)

print 'after:  c =', c
print

c.sort()
CheckVector('sort(c)', '12345678', c, [1,2,3,4,5,6,7,8])
