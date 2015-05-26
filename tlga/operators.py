# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy  import zeros, ones, hstack

from random import Random, RandInt, FlipCoin

def SimpleChromo(x, n):
    """
    SimpleChromo splits x into n unequal parts
    """
    vals = Random(n)
    sumv = sum(vals)
    return x * vals / sumv


def Fitness(Y):
    """
    Fitness function: map objective function into [0, 1]
     Y -- objective values
    """
    ymin, ymax = min(Y), max(Y)
    if abs(ymax - ymin) < 1e-14: return ones(len(Y))
    return (ymax - Y) / (ymax - ymin)


def SortPop(C, Y, F):
    """
    SortPop sort individuals by fitness (decreasing order)
     C -- chromosomes/population
     Y -- objective values
     F -- fitness
    """
    I = F.argsort()[::-1] # the [::-1] is a trick to reverse the sorting order
    C = C[I]              # sorted chromosomes
    Y = Y[I]              # sorted objective values
    F = F[I]              # sorted fitness
    return C, Y, F


def RouletteSelect(M, n, sample=None):
    """
    RouletteSelect selects n individuals
     M -- cumulated probabilities
    """
    if sample==None: sample = Random(n)
    S = zeros(n, dtype=int) # selected individuals
    for i, s in enumerate(sample):
        for j, m in enumerate(M):
            if m > s:
                S[i] = j
                break
    return S


def FilterPairs(S):
    """
    FilterPairs generates 2 x ninds/2 lists from selected individuals
    try to avoid repeated indices in pairs
    """
    ninds = len(S)
    A = zeros(ninds/2, dtype=int)
    B = zeros(ninds/2, dtype=int)
    for i in range(ninds/2):
        a, b = S[2*i], S[2*i+1]
        if a == b:
            for s in S:
                if s != a:
                    b = s
                    break
        A[i], B[i] = a, b
    return A, B


def CrossoverFloat(A, B, pc=0.8):
    """
    CrossoverFloat performs the crossover in a population with float point numbers
    Input:
      A  -- chromosome of parent
      B  -- chromosome of parent
      pc -- probability of crossover
    Output:
      a -- chromosome of offspring
      b -- chromosome of offspring
    """
    if FlipCoin(pc):
        nbases = len(A)
        pos = RandInt(1, nbases-1)
        a = hstack([A[:pos], B[pos:]])
        b = hstack([B[:pos], A[pos:]])
    else:
        a, b = A.copy(), B.copy()
    return a, b


def MutationFloat(c, pm=0.01, coef=1.1):
    """
    MutationFloat performs mutation in an individual with float point numbers
    Input:
      c    -- chromosome
      pm   -- probability of mutation
      coef -- coefficient to increase or decrease bases
    Output:
      c -- modified (or not) chromosome
    """
    if FlipCoin(pm):
        nbases = len(c)
        bmax = max(c)
        pos = RandInt(0, nbases)
        if FlipCoin(0.5): c[pos] += bmax * coef
        else:             c[pos] -= bmax * coef
    return c
