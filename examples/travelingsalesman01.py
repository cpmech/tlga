# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import sys

from numpy import array, sqrt, arange
from pylab import subplot, text, plot, axis, xticks, yticks, show

from tlga.randnums  import Seed, Shuffle
from tlga.output    import PrintPop, Gll, SetForPng, Save
from tlga.operators import SimpleChromo, OrdCrossover, OrdMutation
from tlga.solver    import Evolve

# initialise random numbers generator
Seed(1234) # use a fixed seed, so every time we run this code we will get the same results

# location / coordinates of cities
L = array([[ 60, 200],
           [180, 200],
           [ 80, 180],
           [140, 180],
           [ 20, 160],
           [100, 160],
           [200, 160],
           [140, 140],
           [ 40, 120],
           [100, 120],
           [180, 100],
           [ 60,  80],
           [120,  80],
           [180,  60],
           [ 20,  40],
           [100,  40],
           [200,  40],
           [ 20,  20],
           [ 60,  20],
           [160,  20]], dtype=float)

# 'display' function
def xFcn(c): return '-'.join(['%d' % v for v in c])

# objective function
def oFcn(c):
    dist = 0.0
    for i in range(1, len(c)):
        a, b = c[i-1], c[i]
        dist += sqrt((L[b][0]-L[a][0])**2.0 + (L[b][1]-L[a][1])**2.0)
    a, b = c[-1], c[0]
    dist += sqrt((L[b][0]-L[a][0])**2.0 + (L[b][1]-L[a][1])**2.0)
    return dist

# input data
ninds  = 50    # number of individuals: population size
ngen   = 100   # number of generations
pc     = 0.8   # probability of crossover
pm     = 0.01  # probability of mutation
elite  = True  # use elitism
sus    = False # stochastic universal sampling
rnk    = False # ranking
rnkSP  = 1.5   # selective pressure for ranking

# population
C = []
for i in range(ninds):
    I = range(len(L)) # one individual
    Shuffle(I)
    C.append(I)
C = array(C, dtype=int)

# objective values
Y = array([oFcn(c) for c in C]) # objective values

# print initial population
print '\ninitial population:'
PrintPop(C, Y, xFcn)

# define crossover and mutation functions
def cxFcn(A, B): return OrdCrossover(A, B, pc)
def muFcn(c):    return OrdMutation(c, pm)

# run GA
C, Y, OV = Evolve(C, xFcn, oFcn, cxFcn, muFcn, ngen, elite, sus, rnk, rnkSP)
X = [xFcn(c) for c in C]

# print final population
print '\nfinal population:'
PrintPop(C, Y, xFcn)

# print best individual
print '\nbest =', X[0], ' OV =', Y[0]

# check
if 0:
    c_sorted = range(len(L))
    for c in C:
        c.sort()
        if (c != c_sorted).any():
            print c
            raise Exception('inconsistent results')
    print '[1;32mOK[0m'
    sys.exit()

# prepare figure
SetForPng(proport=1.7, fig_width_pt=400)

# draw location of cities
subplot(2, 1, 1)
for i in range(len(L)): text(L[i][0], L[i][1], '%d'%i)
plot(L[:,0], L[:,1], 'ro', label='cities')
axis('equal')
axis([0, 220, 0, 220])
xticks(arange(0, 220, 20))
yticks(arange(0, 220, 20))
Gll('x', 'y')

# plot travelling salesman path
c = C[0]
for i in range(1, len(c)):
    a, b = c[i-1], c[i]
    plot([L[a][0], L[b][0]], [L[a][1], L[b][1]], 'b-')
a, b = c[-1], c[0]
plot([L[a][0], L[b][0]], [L[a][1], L[b][1]], 'b-')

# plot convergence graph
subplot(2, 1, 2)
G = range(ngen+1)
plot(G, OV, 'b.-', label='OV_best=%g'%OV[-1])
Gll('generation', 'y(x)')
Save('/tmp/tsp01.png')
