# Copyright 2012 Dorival de Moraes Pedroso. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import traceback, warnings

from numpy import isnan

from FEMsolver import FEMsolver

def RunFEMsolverSteady(mesh, etype, prms, vb={}, eb={}):
    """
    RunFEMsolverSteady runs FEMsolver (steady case) without raising Exceptions
    Input:
      mesh  -- the FE mesh (see FEMsolver definition)
      etype -- the element type (see FEMsolver definition)
      prms  -- materials and other parameters (see FEMsolver definition)
      vb    -- [optional] vertex boundary conditions (see FEMsolver definition)
      eb    -- [optional] edge boundary conditions (see FEMsolver definition)
    Output:
      sol -- the FEMsolver object or None if errors happened
      err -- an error message or '' if no errors happened
    Notes:
      this function also calls calc_secondary() method of sol
    """
    warnings.filterwarnings('error')
    try:
        sol = FEMsolver(mesh, etype, prms)
        sol.set_bcs(vb=vb, eb=eb)
        sol.solve_steady()
        sol.calc_secondary()
        if not isnan(sol.U).any():
            return sol, ''
    except:
        formatted_lines = traceback.format_exc().splitlines()
        return None, 'ERROR: ' + formatted_lines[-1]
    return None, 'wrong line reached in femaux.py'
