# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from pylab import grid, xlabel, ylabel, legend
from pylab import gca, xticks, text, axis, rcParams
from matplotlib.patches import Rectangle, FancyArrowPatch


def PrintPop(C, Y, xFcn, F=None, P=None, M=None, showC=False):
    """
    PrintPop prints all individuals
     C    -- chromosomes/population
     Y    -- objective values
     xFcn -- converts C to X values for 'display purposes'
     F    -- fitness
     P    -- probabilities
     M    -- cumulated probabilities
    """

    # auxiliary variables
    X = [xFcn(c) for c in C]                  # 'display' values
    m = max([len(str(x)) for x in X])         # string length of one x value
    n = max([len('%g'%y) for y in Y])         # string length of one y value
    n += 1                                    # spacing
    fmt1 = '%' + str(m) + 's%' + str(n) + 's' # formatting code for strings
    fmt2 = '%' + str(m) + 's%' + str(n) + 'g' # formatting code for numbers
    l = m + n                                 # total length of line in table
    if showC:                                 # show chromosomes
        o = max([len(str(c)) for c in C])     # string length of one chromosome
        fmt3 = '%' + str(o) + 's'             # formatting code for chromosomes
        l += 1 + o
    if F != None: l += 8
    if P != None: l += 8
    if M != None: l += 8

    # header of table
    print '=' * l
    print fmt1 % ('x', 'y'),
    if showC: print fmt3 % 'chromosome/bases',
    if F!=None: print '%7s' % 'fitness',
    if P!=None: print '%7s' % 'prob',
    if M!=None: print '%7s' % 'cum.prob',
    print
    print '-' * l

    # values in table
    for i, x in enumerate(X):
        print fmt2 % (x, Y[i]),
        if showC: print fmt3 % str(C[i]),
        if F!=None: print '%7.3f' % F[i],
        if P!=None: print '%7.3f' % P[i],
        if M!=None: print '%7.3f' % M[i],
        print
    print '=' * l


def Gll(xl, yl, withleg=True, legpos=None):
    """
    Gll adds grid, labels and legend
    """
    grid()
    xlabel(xl)
    ylabel(yl)
    if withleg: legend(loc=legpos)


def PlotProbBins(X, P):
    """
    PlotProbBins plots probabilities bins
     X -- population
     P -- probabilities
    """
    rcParams.update({'figure.figsize':[800/72.27,200/72.27]})
    x0, Tk = 0.0, [0.0]
    for i in range(len(X)):
        gca().add_patch(Rectangle([x0, 0], P[i], 0.2, color='#d5e7ed', ec='black', clip_on=0))
        ha = 'center'
        if i==len(X)-1: ha = 'left' # last one
        text(x0+P[i]/2.0, 0.1, '%.1f'%X[i], ha=ha)
        x0 += P[i]
        Tk.append(x0)
    xticks(Tk, ['%.2f'%v for v in Tk])
    axis('equal')
    gca().get_yaxis().set_visible(False)
    for dir in ['left', 'right', 'top']:
        gca().spines[dir].set_visible(False)
    xlabel('cumulated probability')
    grid()
    axis([0, 1, 0, 0.2])


def DrawChromo(key, A, pos, y0, swap_colors, red='#e3a9a9', blue='#c8d0e3'):
    """
    DrawChromo draws one chromosome
    """
    nbases = len(A)
    x0, l = 0.1, 1.0 / float(nbases)
    red, blue = red, blue
    text(x0-0.01, y0+0.05, key, ha='right')
    if swap_colors: red, blue = blue, red
    for i in range(0, pos):
        gca().add_patch(Rectangle([x0, y0], l, 0.1, color=red, ec='black'))
        text(x0+l/2.0, y0+0.05, '%.3f'%A[i], ha='center')
        x0 += l
    for i in range(pos, nbases):
        gca().add_patch(Rectangle([x0, y0], l, 0.1, color=blue, ec='black'))
        text(x0+l/2.0, y0+0.05, '%.3f'%A[i], ha='center')
        x0 += l


def DrawCrossover(A, B, a, b, pos):
    """
    DrawCrossover draws crossover process
    """
    rcParams.update({'figure.figsize':[800/72.27,400/72.27]})
    DrawChromo('A', A, pos, 0.35, 0)
    DrawChromo('B', B, pos, 0.25, 1)
    DrawChromo('a', a, pos, 0.10, 0, blue='#e3a9a9')
    DrawChromo('b', b, pos, 0.00, 0, red='#c8d0e3')
    axis('equal')
    axis([0, 1.2, 0, 0.4])
    gca().get_yaxis().set_visible(False)
    gca().get_xaxis().set_visible(False)
    for dir in ['left', 'right', 'top', 'bottom']:
        gca().spines[dir].set_visible(False)
    gca().add_patch(FancyArrowPatch([0.6,0.25], [0.6, 0.2], fc='#9fffde', mutation_scale=30))
