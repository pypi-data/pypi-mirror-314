# -*- python -*-
# -*- coding: utf-8 -*-
#
#       dxtr.visu.visualize
#
# In this submodule we define a function to visualize the various objects 
# of the dxtr library. This function calls more specific ones, stored in the 
# pyvista and plotly submodules, depending on the type of visualization 
# that we want.
#
#       File author(s):
#           Olivier Ali <olivier.ali@inria.fr>
#
#       File contributor(s):
#           Olivier Ali <olivier.ali@inria.fr>
#           Florian Gascon <florian.gascon@inria.fr>
#
#       File maintainer(s):
#           Olivier Ali <olivier.ali@inria.fr>
#
#       Copyright © by Inria
#       Distributed under the LGPL License..
#       See accompanying file LICENSE.txt or copy at
#           https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# -----------------------------------------------------------------------
from __future__ import annotations
from typing import Optional

from dxtr.complexes import Simplex, SimplicialComplex
from dxtr.cochains import Cochain
from dxtr.utils import typecheck
from .visu_plotly import visualize_with_plotly
from .visu_pyvista import visualize_with_pyvista


@typecheck([Simplex, SimplicialComplex, Cochain])
def visualize(object:Simplex|SimplicialComplex|Cochain,
              library:Optional[str]=None, **kwargs) -> None:
    '''Draw the provided object with the considered library.

    Parameters
    ----------
    object
        The structure to visualize, should be an instance of `Simplex`, 
        `SimplicialComplex` or `Cochain`.
    library, 
        Optional, default is None. The name of the visualization library 
        to use. If specified, should be either 'plotly' or 'pyvista'. 
        See notes for details.
    
    Other Parameters
    ----------------
    degrees
        Optional (default is 'all').
        The (list of) the simplex degree(s) to display.
    highlight
        Optional (default is None).
        Subset of simplices to highlight.
        if given as dict:
            - keys : int. simplex degrees.
            - values : list(int). collection of simplex indices.

    Notes
    -----
      * If no library is specified at calling, the choice will be made 
        depending on the type of the first argument: If object is an instance of 
        `SimplicialComplex`, the `plotly`-based method will be called. If object 
        is of type `Cochain`, the `pyvista`-based method will be called.
      * Use the `plotly`-based method for exploration of `SimplicialComplex` 
        objects for `plotly`-based methods are interactive; therefore better 
        suited to explore visualy the objects.
      * Use the `pyvista`-based methods to visualize `Cochain` objects.
    
    See also
    --------
      * The `_visualize_with_plotly()` function from the `visualize_plotly` 
        sub-module, for details and specific keywords arguments listing.
      * The `_visualize_with_pyvista()` function from the `visualize_pyvista`
        sub-module, for details and specific keywords arguments listing. 
    
    '''
    
    if library is None:
        library = 'pyvista' if isinstance(object, Cochain) else 'plotly'
    
    if library=='plotly':
        visualize_with_plotly(object, **kwargs)
    
    elif library=='pyvista':
        visualize_with_pyvista(object, 
                        fig=kwargs.get('fig', None), 
                        scaling_factor=kwargs.get('scaling_factor', 1), 
                        data_range=kwargs.get('data_range', None),
                        display=kwargs.get('display', True), 
                        layout_parameters=kwargs.get('layout_parameters', {}))
 
 