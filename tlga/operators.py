# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import zeros, ones, hstack, delete, insert

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


def FltCrossover(A, B, pc=0.8):
    """
    FltCrossover performs the crossover in a pair of individuals with float point numbers
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


def FltMutation(c, pm=0.01, coef=1.1):
    """
    FltMutation performs mutation in an individual with float point numbers
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


def IntCrossover(A, B, pc=0.8, method='OX1', cut1=None, cut2=None):
    """
    IntCrossover performs the crossover in a pair of individuals with integer numbers
    that correspond to a ordered sequence, e.g. traveling salesman problem
    Input:
      A      -- chromosome of parent
      B      -- chromosome of parent
      pc     -- probability of crossover
      method -- OX1: order crossover # 1
      cut1   -- position of first cut: use None for random value
      cut2   -- position of second cut: use None for random value
    Output:
      a -- chromosome of offspring
      b -- chromosome of offspring
    """
    if FlipCoin(pc):
        nbases = len(A)
        if cut1==None: cut1 = RandInt(1, nbases-1)
        if cut2==None: cut2 = RandInt(cut1+1, nbases)
        #print 'cut1 =', cut1, ', cut2 =', cut2
        if cut1==cut2: raise Exception('problem with cut1 and cut2')
        a, b = zeros(nbases, dtype=int), zeros(nbases, dtype=int)
        a[cut1 : cut2] = A[cut1 : cut2]
        b[cut1 : cut2] = B[cut1 : cut2]
        #print '\na =', a
        #print 'b =', b
        c = hstack([[v for v in B[cut2 : nbases] if not v in a],
                    [v for v in B[     : cut2  ] if not v in a]])
        d = hstack([[v for v in A[cut2 : nbases] if not v in b],
                    [v for v in A[     : cut2  ] if not v in b]])
        #print 'c =', c
        #print 'd =', d, '\n'
        a[cut2:] = c[:nbases-cut2]
        a[:cut1] = c[nbases-cut2:]
        b[cut2:] = d[:nbases-cut2]
        b[:cut1] = d[nbases-cut2:]
    else:
        a, b = A.copy(), B.copy()
    return a, b


def IntMutation(c, pm=0.01, method='DM', cut1=None, cut2=None, ins=None):
    """
    IntMutation performs the mutation in an individual with integer numbers
    corresponding to a ordered sequence, e.g. traveling salesman problem
    Input:
      c      -- chromosome
      pm     -- probability of mutation
      method -- DM: displacement mutation
      cut1   -- position of first cut: use None for random value
      cut2   -- position of second cut: use None for random value
      ins    -- position in *cut* slice (v) after which the cut subtour (u) is inserted
    Output:
      c -- modified (or not) chromosome
    """
    if FlipCoin(pm):
        nbases = len(c)
        if cut1==None: cut1 = RandInt(1, nbases-1)
        if cut2==None: cut2 = RandInt(cut1+1, nbases)
        if cut1==cut2: raise Exception('problem with cut1 and cut2')
        u = c[cut1 : cut2]
        v = delete(c, range(cut1, cut2))
        if ins==None: ins = RandInt(0, len(v))
        #print 'u    =', u
        #print 'v    =', v
        #print 'cut1 =', cut1, ' cut2 =', cut2, ' ins =', ins
        c = insert(v, ins+1, u)
    return c

