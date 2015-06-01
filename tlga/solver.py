# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import array, cumsum, zeros

from operators import Fitness, SortPop, Ranking, RouletteSelect, SUSselect, FilterPairs

def Evolve(C, xFcn, oFcn, cxFcn, muFcn, ngen=10, elite=True, sus=False, rnk=False, rnkSP=1.2,
        verb=False, showC=False):
    """
    Evolve solves minimisation problems with a simple genetic algorithm
    Input:
      C     -- all chromosomes == population
      xFcn  -- 'display' function x(c)
      oFcn  -- objective function y(c)
      cxFcn -- crossover function cx(c)
      muFcn -- mutation function mu(c)
      ngen  -- number of generations
      elite -- use elitism
      verb  -- verbose
      showC -- also show chromosomes if verbose
      sus   -- use Stochastic Universal Sampling selection instead of Roulette Wheel
      rnk   -- use ranking
      rnkSP -- ranking selective pressure
    Output:
      C  -- new population (sorted with best first)
      Y  -- new objective values (sorted with best first)
      OV -- best objective values during all generations
    """

    # convert C from list to array
    if isinstance(C, list):
        if isinstance(C[0], int): C = array(C, dtype=int)
        else: C = array(C, dtype=float)

    # objective values
    Y = array([oFcn(c) for c in C]) # objective values
    ninds = len(C)
    nbases = len(C[0])

    # fitness and probabilities (sorted)
    F = Fitness(Y)
    C, Y, F = SortPop(C, Y, F)
    if rnk: F = Ranking(ninds, rnkSP)
    P = F / sum(F)
    M = cumsum(P)

    # results
    OV = zeros(ngen+1)
    OV[0] = Y[0] # best first objective value

    # evolution
    for gen in range(ngen):

        # best individual
        bestC = C[0].copy()
        bestY = Y[0]

        # print generation
        if verb:
            print
            PrintPop(C, Y, xFcn, F, showC=showC)

        # selection
        if sus: S = SUSselect(M, ninds)
        else:   S = RouletteSelect(M, ninds)
        idxA, idxB = FilterPairs(S)

        # reproduction
        Cnew = [] # new chromosomes
        for k in range(ninds/2):

            # parents
            A, B = C[idxA[k]], C[idxB[k]]

            # crossover
            a, b = cxFcn(A, B)

            # mutation
            a = muFcn(a)
            b = muFcn(b)

            # new individuals
            Cnew.append(a)
            Cnew.append(b)

        # new population
        C = array(Cnew)
        Y = array([oFcn(c) for c in C]) # objective values
        F = Fitness(Y)

        # elitism
        if elite:
            I = F.argsort()[::-1] # the [::-1] is a trick to reverse the sorting order
            best  = I[0]
            worst = I[ninds-1]
            if bestY < Y[best] and bestY < Y[worst]:
                C[worst] = bestC
                Y[worst] = bestY
                F = Fitness(Y)

        # probabilities (sorted)
        C, Y, F = SortPop(C, Y, F)
        if rnk: F = Ranking(ninds, rnkSP)
        P = F / sum(F)
        M = cumsum(P)

        # objective values
        OV[gen+1] = Y[0] # best current objective value

    # results
    return C, Y, OV
