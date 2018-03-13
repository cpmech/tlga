# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import numpy as np
import matplotlib.pyplot as plt

from tlga.output import Gll, SetForPng, Save

# location / coordinates of cities
L = np.array([[ 60, 200],
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

# prepare figure
SetForPng(1, 300)

# draw location of cities
for i in range(len(L)):
    plt.text(L[i][0], L[i][1], '%d'%i)
plt.plot(L[:,0], L[:,1], 'ro')
plt.axis('equal')
plt.axis([0, 220, 0, 220])
plt.xticks(np.arange(0, 220, 20))
plt.yticks(np.arange(0, 220, 20))
Gll('x', 'y')

# save
Save('/tmp/cities1.png')
