# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import pi, sin, array, linspace
from pylab import subplot, plot, show

from tlga.randnums  import Seed, FltRand
from tlga.output    import PrintPop, Gll
from tlga.operators import SimpleChromo, FltCrossover, FltMutation
from tlga.solver    import Evolve

# input data
ninds  = 10    # number of individuals: population size
nbases = 5     # number of bases in chromosome
ngen   = 5     # number of generations
pc     = 0.8   # probability of crossover
pm     = 0.01  # probability of mutation
elite  = True  # use elitism

# initialise random numbers generator
Seed(1111) # use a fixed seed, so every time we run this code we will get the same results

# 'display' function
def xFcn(c): return str(sum(c))

# 'greater than' penalty function: a must be greater than b
def gtPenalty(a, b, penaltyM=1000.0):
    if a > b: return 0.0
    return penaltyM * (b - a)

# objective function
xmin, xmax = 0.0, 4.0*pi
def y(x): return -x * sin(x)
def oFcn(c, nbases):
    x = sum(c)
    return y(x) + gtPenalty(x, xmin) + gtPenalty(xmax, x)

# generate nind numbers between 0 and 4*pi
xmin, xmax = 0.0, 4.0*pi
X = FltRand(ninds, xmin, xmax)

# population == all chromosomes
C = [SimpleChromo(x, nbases) for x in X] # split x into random parts

# first objective values
Y = [oFcn(c, nbases) for c in C]

# print initial population
print '\ninitial population:'
PrintPop(C, Y, xFcn, showC=True)

# plot curve
subplot(2, 1, 1)
xcurve = linspace(xmin, xmax, 101)
plot(xcurve, y(xcurve), label='y(x)')
plot(X, Y, 'ro', label='initial population')

# define crossover and mutation functions
def cxFcn(A, B): return FltCrossover(A, B, pc)
def muFcn(c):    return FltMutation(c, pm)

# run GA
C, Y, OV = Evolve(C, xFcn, oFcn, cxFcn, muFcn, ngen, elite)
X = [xFcn(c) for c in C]

# print final population
print '\nfinal population:'
PrintPop(C, Y, xFcn)

# print best individual
print '\nbest =', X[0], ' OV =', Y[0]

# plot points on curve
subplot(2, 1, 1)
plot(X, Y, 'k*', label='final population')
plot(X[0], Y[0], 'gs', label='best')
Gll('x', 'y', legpos='upper left')

# plot convergence graph
subplot(2, 1, 2)
G = range(ngen+1)
plot(G, OV, 'b.-', label='x=%s,y=%g'%(X[0],Y[0]))
Gll('generation', 'y(x)')
show()
