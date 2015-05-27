# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import array

from tlga.random    import Seed
from tlga.operators import OrdCrossover

from testing import CheckVector

# initialise random numbers generator
#Seed(1234) # use a fixed seed, so every time we run this code we will get the same results

# example 1 -----------------------------------------------------------------------------
print 'example 1 -----------------------------------------------------------------------------'

A = array([1,2,3,4,5,6,7,8], dtype=int)
B = array([2,4,6,8,7,5,3,1], dtype=int)

print
print 'A =', A
print 'B =', B
print

a, b = OrdCrossover(A, B, pc=1, cut1=2, cut2=5)

print 'a =', a
print 'b =', b
print

CheckVector('a', 'a_sol', a, [8,7,3,4,5,1,2,6])
CheckVector('b', 'b_sol', b, [4,5,6,8,7,1,2,3])
a.sort()
b.sort()
CheckVector('sort(a)', '12345678', a, [1,2,3,4,5,6,7,8])
CheckVector('sort(b)', '12345678', b, [1,2,3,4,5,6,7,8])

# example 2 -----------------------------------------------------------------------------
print '\nexample 2 -----------------------------------------------------------------------------'

A = array([1,3,5,7,6,2,4,8], dtype=int)
B = array([5,6,3,8,2,1,4,7], dtype=int)

print
print 'A =', A
print 'B =', B
print

a, b = OrdCrossover(A, B, pc=1, cut1=3, cut2=6)

print 'a =', a
print 'b =', b
print

CheckVector('a', 'a_sol', a, [3,8,1,7,6,2,4,5])
CheckVector('b', 'b_sol', b, [5,7,6,8,2,1,4,3])
a.sort()
b.sort()
CheckVector('sort(a)', '12345678', a, [1,2,3,4,5,6,7,8])
CheckVector('sort(b)', '12345678', b, [1,2,3,4,5,6,7,8])

# example 3 -----------------------------------------------------------------------------
print '\nexample 3 -----------------------------------------------------------------------------'

A = array([1,2,3,4,5,6,7,8], dtype=int)
B = array([2,4,6,8,7,5,3,1], dtype=int)

print
print 'A =', A
print 'B =', B
print

a, b = OrdCrossover(A, B, pc=1)

print 'a =', a
print 'b =', b
print

a.sort()
b.sort()
CheckVector('sort(a)', '12345678', a, [1,2,3,4,5,6,7,8])
CheckVector('sort(b)', '12345678', b, [1,2,3,4,5,6,7,8])
