# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import array, zeros, ones, hstack, delete, insert, arange

from randnums import FltRand, IntRand, FlipCoin

def SimpleChromo(x, nbases):
    """
    SimpleChromo splits x into 'nbases' unequal parts
    Input:
      x -- a single number or a list whose size equals the number of genes
    Output:
      c -- the chromosome (numpy.ndarray)
    Note:
      If x is a list, ngenes = len(x) and then:
      If ngenes > 1, each gene is split into 'nbases' and the following
      chromosome structure is assumed:

          c = [0, 1, 2, ... nbases-1,  0, 1, 2, ... nbases-1]
               \___________________/   \___________________/
                      gene # 0               gene # 1
    """
    if isinstance(x, float):
        vals = FltRand(nbases)
        sumv = sum(vals)
        return x * vals / sumv
    if isinstance(x, list): x = array(x)
    ngenes = len(x)
    c = zeros(nbases * ngenes)
    for i, v in enumerate(x):
        vals = FltRand(nbases)
        sumv = sum(vals)
        a = i * nbases
        b = a + nbases
        c[a:b] = v * vals / sumv
    return c


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


def Ranking(ninds, sp=1.2):
    """
    Ranking computes fitness corresponding to a linear ranking
    Input:
      ninds -- number of individuals
      sp    -- selective pressure; must be inside [1, 2]
    Output:
      F -- ranked fitnesses
    """
    if sp < 1.0 or sp > 2.0: sp = 1.2
    F = zeros(ninds)
    for i in range(ninds):
        F[i] = 2.0 - sp + 2.0*(sp-1.0)*float(ninds-i-1)/float(ninds-1)
    return F


def RouletteSelect(M, n, sample=None):
    """
    RouletteSelect selects n individuals
    Input:
      M      -- cumulated probabilities (from sorted population)
      sample -- a list of random numbers
    Output:
      S -- selected individuals (indices)
    """
    if sample==None: sample = FltRand(n)
    S = zeros(n, dtype=int) # selected individuals
    for i, s in enumerate(sample):
        for j, m in enumerate(M):
            if m > s:
                S[i] = j
                break
    return S


def SUSselect(M, n, pb=None):
    """
    SUSselect performs the Stochastic-Universal-Sampling selection
    It selects n individuals
    Input:
      M  -- cumulated probabilities (from sorted population)
      pb -- one random number corresponding to the first probability (pointer/position)
    Output:
      S -- selected individuals (indices)
    """
    dp = 1.0 / float(n)
    if pb == None: pb = FltRand(1, 0.0, dp)
    S = zeros(n, dtype=int) # selected individuals
    for i in range(n):
        j = 0
        while pb > M[j]: j += 1
        pb += dp
        S[i] = j
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
        pos = IntRand(1, nbases-1)
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
        pos = IntRand(0, nbases)
        if FlipCoin(0.5): c[pos] += bmax * coef
        else:             c[pos] -= bmax * coef
    return c


def OrdCrossover(A, B, pc=0.8, method='OX1', cut1=None, cut2=None):
    """
    OrdCrossover performs the crossover in a pair of individuals with integer numbers
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
        if cut1==None: cut1 = IntRand(1, nbases-1)
        if cut2==None: cut2 = IntRand(cut1+1, nbases)
        if cut1==cut2: raise Exception('problem with cut1 and cut2')
        a, b = zeros(nbases, dtype=int), zeros(nbases, dtype=int)
        m, n = A[cut1 : cut2], B[cut1 : cut2]
        a[cut1 : cut2] = m
        b[cut1 : cut2] = n
        #print '\ncut1 =', cut1, ', cut2 =', cut2
        #print 'A =', A
        #print 'B =', B
        #print 'a =', a
        #print 'b =', b
        c = hstack([[v for v in B[cut2 : nbases] if not v in m],
                    [v for v in B[     : cut2  ] if not v in m]])
        d = hstack([[v for v in A[cut2 : nbases] if not v in n],
                    [v for v in A[     : cut2  ] if not v in n]])
        #from numpy import array
        #print 'c =', array(c, dtype=int)
        #print 'd =', array(d, dtype=int), '\n'
        a[cut2:] = c[:nbases-cut2]
        a[:cut1] = c[nbases-cut2:]
        b[cut2:] = d[:nbases-cut2]
        b[:cut1] = d[nbases-cut2:]
    else:
        a, b = A.copy(), B.copy()
    return a, b


def OrdMutation(c, pm=0.01, method='DM', cut1=None, cut2=None, ins=None):
    """
    OrdMutation performs the mutation in an individual with integer numbers
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
        if cut1==None: cut1 = IntRand(1, nbases-1)
        if cut2==None: cut2 = IntRand(cut1+1, nbases)
        if cut1==cut2: raise Exception('problem with cut1 and cut2')

        # create copy of c
        c = c.copy()

        # new method
        if True:

            # lengths and insertion point
            nc = len(c)
            ncut = cut2 - cut1 # number of cut items
            nrem = nc - ncut   # number of remaining items
            if ins==None: ins = IntRand(0, nrem)

            # auxiliary map: old => new index
            o2n = arange(nc)
            for i in range(nc):
                if   i < cut1: o2n[i] = i      # index is unchanged
                elif i < cut2: o2n[i] = -1     # mark cut items with -1
                else:          o2n[i] = i-ncut # shift items after cut to the left
            k = 1 # increment for index of new cut item
            for i in range(nc):
                if o2n[i] > ins:
                    o2n[i] += ncut # shift right to accomodate cut items
                if o2n[i] < 0:
                    o2n[i] = ins+k # put cut items after 'ins'
                    k += 1

            # copy items to the right place
            cc = c.copy()
            for o, n in enumerate(o2n):
                c[n] = cc[o]

        # this method, using 'insert', apparently fails in some 
        # versions of numpy and windows
        if False:
            u = c[cut1 : cut2]
            v = delete(c, range(cut1, cut2))
            if ins==None: ins = IntRand(0, len(v))
            #print 'u    =', u
            #print 'v    =', v
            #print 'cut1 =', cut1, ' cut2 =', cut2, ' ins =', ins
            c = insert(v, ins+1, u)
    return c


# test
if __name__ == "__main__":

    from numpy   import cumsum
    from pylab   import show, plot
    from testing import CheckVector
    from output  import PlotProbBins, Gll

    # scalar chromosome
    print '\n#################### scalar chromosome #######################'
    x = 5.0
    c = SimpleChromo(x, 5)
    X = sum(c)
    print 'x =', x
    print 'c =', c
    print 'X =', X
    if abs(x - X) > 1e-14: raise Exception('test failed')

    # array chromosome
    print '\n#################### array chromosome #######################'
    x = [5.0, 8.0, 7.0]
    c = SimpleChromo(x, 5)
    x0 = sum(c[  : 5])
    x1 = sum(c[ 5:10])
    x2 = sum(c[10:  ])
    print 'x =', x
    print 'c =', c
    print 'x0 =', x0
    print 'x1 =', x1
    print 'x2 =', x2
    if abs(x0 - 5.0) > 1e-14: raise Exception('test failed')
    if abs(x1 - 8.0) > 1e-14: raise Exception('test failed')
    if abs(x2 - 7.0) > 1e-14: raise Exception('test failed')

    # roulette wheel selection
    print '\n#################### roulette selection #####################'
    F = array([2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.2, 0.0])
    P = F / sum(F)
    M = cumsum(P)
    S = RouletteSelect(M, 6, sample=[0.81, 0.32, 0.96, 0.01, 0.65, 0.42])
    print 'F =', F
    print 'P =', P
    print 'M =', M
    print 'S =', S
    CheckVector('S','Scor', S, [5, 1, 8, 0, 4, 2])
    #PlotProbBins(range(len(P)), P)
    #show()

    # SUS selection
    print '\n############# stochastic universal selection ################'
    S = SUSselect(M, 6, pb=0.1)
    print 'S =', S
    CheckVector('S','Scor', S, [0, 1, 2, 3, 5, 7])

    # ranking
    print '\n######################## ranking ############################'
    n = 11
    for i, sp in enumerate([1.0, 1.1, 1.5, 2.0]):
        F = Ranking(n, sp=sp)
        print 'F(sp=%g) ='%sp, F
        plot(range(n), F, label='sp=%g'%sp)
        if i==0: CheckVector('F','Fcor', F, ones(n))
        #if i==1: CheckVector('F','Fcor', F, [1.1,1.08,1.06,1.04,1.02,1,0.98,0.96,0.94,0.92,0.9])
        if i==3: CheckVector('F','Fcor', F, [2,1.8,1.6,1.4,1.2,1.0,0.8,0.6,0.4,0.2,0])
    #Gll('i', 'F')
    #show()
