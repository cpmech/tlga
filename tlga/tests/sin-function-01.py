# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import pi, sin, array, linspace
from pylab import subplot, plot, show

from tlga.random    import Seed, Random
from tlga.operators import SimpleChromo, CrossoverFloat, MutationFloat
from tlga.output    import PrintPop, Gll
from tlga.solver    import evolve

# initialise random numbers generator
Seed(1234) # use a fixed seed, so every time we run this code we will get the same results

# 'display' function
def xFcn(c): return str(sum(c))

# objective function
xmin, xmax = 0.0, 4.0*pi
def y(x): return -x * sin(x)
def oFcn(c):
    x = sum(c)
    if x < xmin or x > xmax: # constraints
        return 100.0*(1.0+abs(x))
    return y(x)

# input data
ninds  = 10    # number of individuals: population size
nbases = 5     # number of bases in chromosome
ngen   = 10    # number of generations
pc     = 0.8   # probability of crossover
pm     = 0.01  # probability of mutation
elite  = 1     # use elitism
verb   = False # verbose

# population
X = Random(ninds, xmin, xmax) # generate nind numbers between 0 and 4*pi
X = array(X, dtype=int)       # truncate values (just for the sake of showing nice numbers)
X = array(X, dtype=float)     # revert to float
C = array([SimpleChromo(x, nbases) for x in X])

# objective values
Y = array([oFcn(c) for c in C])

# print initial population
print '\ninitial population:'
PrintPop(C, Y, xFcn, showC=True)

# plot curve
subplot(2, 1, 1)
xcurve = linspace(xmin, xmax, 101)
plot(xcurve, y(xcurve), label='y(x)')
plot(X, Y, 'ro', label='final population')

# define crossover and mutation functions
def cxFcn(A, B): return CrossoverFloat(A, B, pc)
def muFcn(c): return MutationFloat(c, pm)

# run GA
C, Y, OV = evolve(C, xFcn, oFcn, cxFcn, muFcn, ngen, elite, verb)
X = [xFcn(c) for c in C]

# print final population
print '\nfinal population:'
PrintPop(C, Y, xFcn)

# print best individual
print '\nbest =', X[0], ' OV =', Y[0]

# plot points on curve
subplot(2, 1, 1)
plot(X, Y, 'k*', label='final population')
Gll('x', 'y', legpos='upper left')

# plot convergence graph
subplot(2, 1, 2)
G = range(ngen+1)
plot(G, OV, 'b.-', label='x=%s,y=%g'%(X[0],Y[0]))
Gll('generation', 'y(x)')
show()
