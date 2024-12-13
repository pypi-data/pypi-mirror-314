# -*- python -*-
# -*- coding: utf-8 -*-
#
#       dxtr.complexes.simplicialcomplex
#
# This file contains one class:
#     - `SimplicialComplex`
# and a few functions usefull to set the geometrical properties of this class.
#
#       File author(s):
#           Olivier Ali <olivier.ali@inria.fr>
#
#       File contributor(s):
#           Olivier Ali <olivier.ali@inria.fr>
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
from pathlib import Path
from typing import Optional, Iterable

import numpy as np
import numpy.linalg as lng

from dxtr import logger
from dxtr.utils.typecheck import typecheck, valid_input
from dxtr.complexes import AbstractSimplicialComplex
from dxtr.math.geometry import volume_simplex

class SimplicialComplex(AbstractSimplicialComplex):
    '''Embodies the concept of simplicial complex.'''

    def __init__(self, indices: list[list[int]],
                 vertices: Optional[Iterable[Iterable[float]]]=None, 
                 name: Optional[str]=None) -> None:
        
        super().__init__(indices, name)
        
        if _isproperly_embedded(self, vertices):
            self.build_geometry(vertices)


    def __str__(self) -> str:
        description = f'{self.dim}D'
        description += ' Abstract ' if self.isabstract else ' '
        description += f'Simplicial Complex of shape {self.shape}, '
        if not self.isabstract:
            description += f'embedded in R^{self.emb_dim}.'
        return description

    @classmethod
    def from_file(cls, path:str, 
                  name: Optional[str]=None) -> SimplicialComplex:
        '''Instanciates a `SimplicialComplex` from a `.ply` file'''
        
        from dxtr.io import read_ply
        
        indices, vertices = read_ply(path)
        
        return cls(indices, vertices, name)
    
    @valid_input
    def to_file(self, file_name:str, format:Optional[str]='.ply', 
                folder:Optional[str|Path]=None) -> None:
        '''_summary_

        Parameters
        ----------
        file_name
            The name of the file to write on disk.
        format, optional
            The type of file to write, see Notes.
        folder, optional
            The location where to write the file.
        
        Notes
        -----
          * `SimplicialComplexe` instances can be saved as `.fly` or `.vtk`.
          * By default, the chosen format is `.ply`.
        '''
        
        from dxtr.io.write import write_ply, format_path_properly
        from dxtr.utils.wrappers import UGrid

        path = format_path_properly(folder, file_name, format)
        
        if path.suffix=='.ply':
            write_ply(self[-1].vertex_indices, self[0].vertices, path=path)

        elif path.suffix=='.vtk':
            ugrid = UGrid.generate_from(self)
            ugrid.save(path)

    @property
    def name(self) -> str:
        '''Name of the complex.'''
        if self._name is None:
            return self.__str__()[:21]
        else:
            return self._name
            
    @name.setter
    def name(self, new_name:str) -> None:
        '''Sets a custom name for the complex.'''
        self._name = new_name
    
    @property
    def isabstract(self) -> bool:
        '''States if a complex is embedded within a geometrical space or not.
        '''
        return self._isabstract

    @property
    def emb_dim(self) -> int:
        '''Dimension of the embedding euclidean space.
        '''
        return self._embedded_dim

    @property
    def vertices(self) -> np.ndarray[float]:
        '''Returns the vertices corresponding to the 0-simplices.'''
        return self._vertices

    def build_geometry(self, vertices:Iterable[Iterable[float]]) -> None:
        '''Formats the vertices and computes the k-volumes of all simplices.
        '''
        _set_vertices(self, vertices)
        _compute_volumes(self)
    

    def update_geometry(self, displacement:dict[int,np.ndarray[float]]) -> None:
        '''Updates some vertices and the corresponding geometrical properties.

        Parameters
        ----------
        displacement
            - keys: The indices of the vertices to move.
            - values: The displacement to add to the selected vertices.
        
        Notes
        -----
            * When applied to a simplicial complex,
              the only recomputed geometrical property is the simplex volume.
        '''
        
        moved_vids = list(displacement.keys())
        dplcmt = list(displacement.values())
        
        self._vertices[moved_vids] += dplcmt 
        _compute_volumes(self, surrounding=moved_vids)


# ################# #
# Usefull functions #
# ################# #


def _isproperly_embedded(complex:AbstractSimplicialComplex,
                       vertices:Optional[Iterable[Iterable[float]]]) -> bool:
    '''Checks if the provided vertices have the proper size and shape.

    Note
    -----
        Also sets the values of two inner attributes of the class:
        * _isabstract
        * _embedded_dim
    '''

    try:
        assert vertices is not None, 'No vertices are defined.'
        assert len(vertices) == complex.shape[0], (
            'The number of position vectors'+
            'do not match the number of 0-simplices.')
        
        l0 = len(vertices[0])
        
        assert complex.dim <= l0, (
            f'a {complex.dim}-complex cannot be embedded in a {l0}D space.')
        assert all(len(p) == l0 for p in vertices[1:]), (
            'The vertices vectors do not all have the same dimension.')
        
        complex._isabstract = False
        complex._embedded_dim = l0
        logger.info(f'Embedding the ASC in R^{complex._embedded_dim}')
        return True

    except AssertionError as msg:
        complex._isabstract = True
        complex._embedded_dim = None
        logger.warning(msg)
        return False


def _set_vertices(complex:SimplicialComplex,
                  vertices:Iterable[Iterable[float]]) -> None:
    '''Set the vertices to each group of k-simplices with the complex.
    '''

    complex._vertices = np.asarray(vertices, dtype=float)
    
    for k, mdl in enumerate(complex):
        mdl.set('vertices', complex._vertices)


def _compute_volumes(complex:SimplicialComplex,
                    surrounding:Optional[list[int]]=None) -> None:
    '''Computes the volume of simplices within a complex.

    Parameters
    ----------
    Complex
        The SimplicialComplex to consider
    Surrounding
        Optional (default is None).
        If None, volumes are computed for all simplices within the complex.
        Else, a list of indices 0-simplices must be provided. In this case, 
        only the volumes of the adjacent simplices to the ones listed are
        computed.

    Notes
    -----
      * By convention, the volume of 0-simplices is set to 1.
      * The computed volumes are unsigned.

    See also
    --------
        dxtr.math.geometry.volume_simplex:
        The function used to compute the volume of a given simplex.
    '''
    if surrounding is None:
        for k, mdl in enumerate(complex):
            if k == 0:
                splx_volumes = np.ones(mdl.size)
            else:
                vids = np.array(complex.faces(k, 0))
                splx_volumes = np.array([volume_simplex(pts)
                                        for pts in complex._vertices[vids]])

            mdl.set('volumes', splx_volumes)
    
    else:
        for k in range(1, complex.dim+1):
            mdl = complex[k]
            sids = complex.star(surrounding, 0)[k]

            vids = np.array([complex.closure({k: idx})[0] 
                             for idx in range(mdl.size)])[sids]

            mdl._volumes[sids] = np.array([volume_simplex(pts)
                                        for pts in complex[0]._vertices[vids]])


@typecheck(SimplicialComplex)
def primal_edge_vectors(of:SimplicialComplex, normalized:bool=False
                 ) -> np.ndarray[float]:
    '''Computes the primal and/or dual edge vectors of a `SimplicialComplex`.

    Parameters
    ----------
    of
        The `SimplicialManifold` of interest.
    
    normalized
        If true the returned vectors have length one.

    Returns
    -------
        An array of shape (N1, D), N1 = number of 1-simplices, 
        D = embedding dimension.
    
    Notes
    -----
      * We require a `SimplicialManifold` as input because we use the 
        `circumcenters` property.
      * This algorithm do not take into consideration the orientation of 
        1-simplices. This might be a problem for some application in the 
        future. This limitation must be rememebered.
    '''

    mfld = of

    edges = mfld[0].coboundary @ mfld[0].vertices
    
    if normalized:
        edges /= lng.norm(edges, axis=-1).reshape(*edges.shape[:-1], 1)

        # to deal with the edges of size 0 on the borders of open complexes.
        if np.isnan(edges).any(): edges[np.where(np.isnan(edges))] = 0

    return edges

