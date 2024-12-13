# -*- python -*-
# -*- coding: utf-8 -*-
#
#       dxtr.math.topology
#
# This submodule contains useful functions to compute
# topological properties on abstract simplicial complexes.
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
#       https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# -----------------------------------------------------------------------
from __future__ import annotations

from typing import Iterable, Optional

import numpy as np
import scipy.sparse as sp
from dxtr import logger


def star(chain_complex:list[sp.csr_matrix[int]],
         simplex_indices:dict[int, list[int]]) -> dict[int, list[int]]:
    '''Gets the list of all cofaces of a given simplex.'''

    cochain_complex = [mtrx.T for mtrx in chain_complex[1:]]
    Nn = chain_complex[-1].shape[1]
    zero_mtrx = sp.csr_matrix((Nn, 1), dtype=int)
    cochain_complex.append(zero_mtrx.T)

    n = len(cochain_complex)
    kmin = min(simplex_indices.keys())

    star = {k: [] for k in range(kmin, n)}

    for k, ids in simplex_indices.items():
        
        if not isinstance(ids, Iterable):
            ids = [ids]
        elif not isinstance(ids, list):
            ids = list(ids)

        star[k] += ids

        coboundary = abs(cochain_complex[k][:, ids])
        for q in range(k+1, n):
            star[q] += list(coboundary.nonzero()[0])
            coboundary = abs(cochain_complex[q]) @ coboundary

    return {k: list(np.unique(cbnd).astype(int))
            for k, cbnd in star.items()
            if len(cbnd) != 0}


def closure(chain_complex:list[sp.csr_matrix[int]],
            simplices:dict[int, list[int]]) -> dict[int, list[int]]:
    '''Gets the smallest simplicial complex containing the given simplices.'''

    kmax = max(simplices.keys())

    if kmax < 0: return {0: []}

    closure = {k: [] for k in range(kmax+1)}

    for k, ids in sorted(simplices.items())[::-1]:
        
        if not isinstance(ids, Iterable):
            ids = [ids]
        elif not isinstance(ids, list):
            ids = list(ids)

        closure[k] += ids

        boundary = abs(chain_complex[k][:, ids])
        for q in range(k-1, -1, -1):
            closure[q] += list(boundary.nonzero()[0])
            boundary = abs(chain_complex[q]) @ boundary
            
    return {k: list(np.unique(bnd).astype(int))
            for k, bnd in closure.items()}


def link(chain_complex:list[sp.csr_matrix[int]],
         simplices:dict[int, list[int]]) -> dict[int, list[int]]:
    '''Gets the topological sphere surrounding the given simplices.'''

    closure_star = closure(chain_complex, star(chain_complex, simplices))
    star_closure = star(chain_complex, closure(chain_complex, simplices))

    link = {k: list(set(closure_star[k]) - set(star_closure[k]))
            for k in closure_star.keys()}

    return {k: sorted(splcs)
            for k, splcs in link.items()
            if len(splcs) > 0}


def border(chain_complex:list[sp.csr_matrix[int]],
           simplices:Optional[dict[int, list[int]]]=None
           ) -> dict[int, list[int]]:
    '''Gets the subcomplex boundary of a set of simplices.'''

    kmax = max(simplices.keys())
    
    top_sids = simplices[kmax]
    top_boundary = chain_complex[kmax][:, top_sids]

    outer_face_ids = np.where(abs(top_boundary.sum(axis=1)) == 1)[0]
    return closure(chain_complex, {kmax-1: outer_face_ids})


def interior(chain_complex:list[sp.csr_matrix[int]],
             simplices:dict[int, list[int]]|None=None) -> dict[int, list[int]]:
    '''Computes the interior of a subset of simplices.'''

    clsr = closure(chain_complex, simplices)
    borders = border(chain_complex, clsr)

    interior = {k: list(set(splcs_ids) - set(borders[k]))
                if k in borders.keys()
                else splcs_ids
                for k, splcs_ids in clsr.items()}

    return {k: int_ids for k, int_ids in interior.items()
            if int_ids}


def complex_simplicial_partition(chain_complex:list[sp.csr_matrix[int]],
                                 lowest_dim:int=0) -> list[np.ndarray[int]]:
    '''Expands an abstract dual cell complex into simplices.

    Parameters
    ----------
    chain_complex
        The chain complex (i.e. list of incidence matrices) to consider.
    lowest_dim, optional
        default is 0. The topological dimension (k) of k-simplicies to start 
        the enumeration with.

    Returns
    -------
    list[np.ndarray[int]]
      list of length n, starts with n-dual cells up to 1-dual cells.
      The list kth element is a array of shape (N, n-k+1) where N corresponds 
      to the number of (n-k) simplices necessary to decompose the dual complex 
      into a simplicial one (where the vertices are the circumcenters of 
      all thep primal simplices).

    Notes
    -----
      * The main purpose of this method is to compute efficiently 
        the covolumes of dual cells.
      * This method computes partition for dual cells of k-simplices
        -- within a n-complex -- up to the (n-1) degree; for the partition 
        of dual cells of n-simplices is trivial.
      * For each array in the output list, the simplex indices are given in the 
        assending order of simplex degree, *i.e.* starting from the lowest 
        simplex to the n-simplices.
      * The chain complex contained within `AbstractSimplicialComplex` 
        has two extra nul matrices at position 0 (first) and -1 (last). 
        These are useful for other stuff but not here, 
        so we start by removing them.
    '''

    indices = []
    
    for bnd in chain_complex[-2:lowest_dim:-1]:
        if len(indices)==0:
            indices.append(np.vstack(bnd.nonzero()).T)
        else:
            new_indices = []
            for ids in np.vstack(bnd.nonzero()).T:
                cfids = np.where(indices[-1][:,0]==ids[-1])[0]
                cfnbr = cfids.shape[0]
                new_indices.append(np.hstack((ids[0]*np.ones((cfnbr, 1),
                                                             dtype=int),
                                              indices[-1][cfids])))
            indices.append(np.vstack(new_indices))

    return indices[::-1]


def cell_simplicial_partition(chain_complex:list[sp.csr_matrix[int]], 
                                   sid:int, k:int) -> list[list[int]]:
    '''Expands a dual cell into simplices and returns their index lists.

    Parameters
    ----------
    chain_complex :
        The chain complex (i.e. list of incidence matrices) to consider.
    sid :
        Index of the k-simplex of interest. The dual cell of which we want to
        partition into sub-simplices.
    k :
        Topological dimension of the k-simplices of interest.
        Should verify k < n. The topological dimension of the dual cell is 
        therefore n-k > 0.

    Returns
    -------
    list[list[int]]
        shape = (n-k+1). Where N is the number of simplices create to
        decompose the the star complex around the provided simplex.

    Notes
    -----
    * Each row of the output corresponds to a simplex formed by 
      the circumcenters of existing simplices of increasing degree.
    '''

    n = len(chain_complex) - 2

    try:
        assert k < n, 'Simplex dim must be strictly smaller than complex dim.'
        assert not isinstance(sid, Iterable), (
            'Do not support lists of indices as argument.')
    
    except AssertionError as msg:
        logger.warning(msg)
        return None
    
    sids = [sid]

    while k < n:
        new_sids = []
        for idx in sids:
            if not isinstance(idx, Iterable): idx = [idx]

            for cf_id in star(chain_complex, {k: idx[-1]})[k+1]:
                new_sids.append(idx+[cf_id])

        sids = new_sids
        k += 1

    return sids


def count_permutations_between(list_1:list[int], 
                               list_2:list[int]) -> Optional[int]:
    '''Counts the number of permutations needed to get from one list to another.

    Parameters
    ----------
    list_1
        The first list to consider.
    list_2
        The second one to consider.

    Returns
    -------
        The sought number of permutations.
    
    Notes
    -----
      * This method do not count the minimal number of permuntations to get one 
        list from the other but rather a number that works.
      * This number of permutation will be useful to compute the relative 
        orientation between neighboring k- and l-simplices ; therefore what 
        matter is not its actual value but its parity (odd or even).
      * It is based on the detection of swap cycles between the two lists, i.e. 
        the sequences of swaps required to sort subsets of the two lists.
      * In order to be generic, the first thing is to work on the list element  
        indices rather than their values themselves. That is why we use the 
        `index_map` dictionnary below.
    '''
    
    try:
        nbr_ids = len(list_1)
        assert len(list_2) == nbr_ids, 'Input lists must have the same length.'
        assert np.isin(list_1, list_2).all(), (
                        'Input lists must contain the same elements.')
    except AssertionError as msg:
        logger.warning(msg)
        return None

    index_map = {value: idx for idx, value in enumerate(list_2)}
    target_indices = [index_map[value] for value in list_1]
    
    visited = [False] * nbr_ids
    
    perm_nbr = 0
    for idx in range(nbr_ids):
        if not visited[idx]:
            perm_nbr += permutation_number_in_swap_cycle(target_indices, idx, 
                                                         visited)

    return perm_nbr


def permutation_number_in_swap_cycle(unsorted_indices:list[int],
                                     starting_index:int, 
                                     visited:list[bool])-> int:
    '''Computes the number of permutations within a swap cycle.

    Parameters
    ----------
    unsorted_indices
        An unsorted list of the n first integers, starting at 0.
    starting_index
        The place on the list where to test for a swap cycle.
    visited
        A list of boolean values of the same size of `unsorted_indices`, 
        saying if the various starting_indices have ready been tasted.

    Returns
    -------
        The desired number of permutations.

    Notes
    -----
      * A swap cycle corresponds to a series of swaps that enable to put back 
        a series of indices in their rightful places.
        Examples: 
        1. in the following unsorted list of indices [2,1,0] there is a 
           swap cycle of size 1 that permits to put '2' and '0' in their 
           correct place: 2->0
        2. in [2,1,3,0] there is a swap cycle of size 2: 2->3->0.
      * The point of the method is to find out if such a cycle starting a given 
        position (`starting_index`) exist. And if so, to compute the number of 
        permutations required to move the corresponding indices to their 
        sorted position.
    '''

    cycle_size = 0
    permutation_number = 0
    idx = starting_index
    
    while not visited[idx]:
        visited[idx] = True
        target_idx = unsorted_indices[idx]
        permutation_number += abs(target_idx-idx)
        cycle_size += 1    
        idx = target_idx
    
    cycle_size -= 1
    
    return permutation_number - cycle_size
