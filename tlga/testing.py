# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from numpy import array

def CheckVector(str_a, str_b, a, b, verb=True):
    a = array(a)
    b = array(b)
    if (a != b).any():
        print '[1;31m ' + str_a + ' != ' + str_b + ':  ', a, ' != ', b, '[0m'
        return
    if verb:
        print str_a + ' == ' + str_b + '  [1;32mOK[0m'
