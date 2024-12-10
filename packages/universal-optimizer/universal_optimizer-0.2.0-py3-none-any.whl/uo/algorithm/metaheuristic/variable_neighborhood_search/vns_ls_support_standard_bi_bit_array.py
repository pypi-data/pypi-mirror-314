""" 
..  _py_minimum_multi_cut_problem_bit_array_solution_vns_support:

The :mod:`~opt.single_objective.comb.minimum_multi_cut_problem.minimum_multi_cut_problem_bit_array_solution_vns_support` 
contains class :class:`~opt.single_objective.comb.minimum_multi_cut_problem.minimum_multi_cut_problem_bit_array_solution_vns_support.MinMultiCutProblemBitArraySolutionVnsSupport`, 
that represents supporting parts of the `VNS` algorithm, where solution of the :ref:`Problem_MinimumMultiCut` have `BitArray` 
representation.
"""
import sys
from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from random import choice

from typing import TypeVar

from bitstring import BitArray

from uo.utils.complex_counter_uniform_ascending import ComplexCounterUniformAscending

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.single_solution_metaheuristic import SingleSolutionMetaheuristic
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support import VnsLocalSearchSupport

A_co = TypeVar("A_co", covariant=True)

class VnsLocalSearchSupportStandardBestImprovementBitArray(VnsLocalSearchSupport[BitArray,A_co]):
    
    def __init__(self, dimension:int)->None:
        """
        Create new `VnsLocalSearchSupportStandardBestImprovementBitArray` instance
        """
        super().__init__(dimension=dimension)

    def copy(self):
        """
        Copy the `VnsLocalSearchSupportStandardBestImprovementBitArray` instance

        :return: new `VnsLocalSearchSupportStandardBestImprovementBitArray` instance with the same properties
        :rtype: `VnsLocalSearchSupportStandardBestImprovementBitArray`
        """
        obj = VnsLocalSearchSupportStandardBestImprovementBitArray(self.dimension)
        return obj

    def local_search(self, k:int, problem:Problem, solution:Solution, 
            optimizer: SingleSolutionMetaheuristic)->bool:
        """
        Executes "best improvement" variant of the local search procedure 
        
        :param int k: int parameter for VNS
        :param `Problem` problem: problem that is solved
        :param `Solution` solution: solution used for the problem that is solved
        :param `SingleSolutionMetaheuristic` optimizer: metaheuristic optimizer that is executed
        :return: result of the local search procedure 
        :rtype: if local search is successful
        """
        if optimizer.should_finish():
            return False
        if k < optimizer.k_min or k > optimizer.k_max:
            return False
        start_sol:Solution = solution.copy()
        best_sol:Solution = solution.copy()
        better_sol_found:bool = False
        # initialize indexes
        indexes:ComplexCounterUniformAscending = ComplexCounterUniformAscending(k, self.dimension)
        in_loop:bool = indexes.reset()
        while in_loop:
            # collect positions for inversion from indexes
            positions:list[int] = indexes.current_state()
            # invert and compare, switch of new is better
            mask:BitArray = BitArray(length=solution.representation.len)
            for i in positions:
                partial_mask = BitArray(length=solution.representation.len)
                partial_mask[-1] = True
                partial_mask.ror(i)
                mask |= partial_mask
            solution.representation ^= mask 
            if optimizer.should_finish():
                solution.copy_from(start_sol)
                return False
            optimizer.write_output_values_if_needed("before_evaluation", "b_e")
            optimizer.evaluation += 1
            solution.evaluate(problem)
            optimizer.write_output_values_if_needed("after_evaluation", "a_e")
            if solution.is_better(best_sol, problem):
                better_sol_found = True
                best_sol.copy_from(solution)
            mask:BitArray = BitArray(length=solution.representation.len)
            for i in positions:
                partial_mask = BitArray(length=solution.representation.len)
                partial_mask[-1] = True
                partial_mask.ror(i)
                mask |= partial_mask
            solution.representation ^= mask 
            # increment indexes and set in_loop according to the state
            in_loop = indexes.progress()
        if better_sol_found:
            solution.copy_from(best_sol)
            return True
        solution.copy_from(start_sol)
        return False
    
    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the vns support structure

        :param delimiter: delimiter between fields
        :type delimiter: str
        :param indentation: level of indentation
        :type indentation: int, optional, default value 0
        :param indentation_symbol: indentation symbol
        :type indentation_symbol: str, optional, default value ''
        :param group_start: group start string 
        :type group_start: str, optional, default value '{'
        :param group_end: group end string 
        :type group_end: str, optional, default value '}'
        :return: string representation of vns support instance
        :rtype: str
        """        
        return 'VnsLocalSearchSupportStandardBestImprovementBitArray'

    def __str__(self)->str:
        """
        String representation of the vns support instance

        :return: string representation of the vns support instance
        :rtype: str
        """
        return self.string_rep('|')

    def __repr__(self)->str:
        """
        Representation of the vns support instance

        :return: string representation of the vns support instance
        :rtype: str
        """
        return self.string_rep('\n')


    def __format__(self, spec:str)->str:
        """
        Formatted the vns support instance

        :param str spec: format specification
        :return: formatted vns support instance
        :rtype: str
        """
        return self.string_rep('|')


