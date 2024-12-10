"""
The :mod:`~uo.algorithm.metaheuristic.genetic_algorithm.ga_mutation_support` module describes the class :class:`~uo.algorithm.metaheuristic.genetic_algorithm.ga_mutation_support.GaMutationSupport`.
"""

from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from abc import ABCMeta, abstractmethod
from typing import TypeVar
from typing import Generic

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.algorithm.metaheuristic.population_based_metaheuristic import PopulationBasedMetaheuristic

R_co = TypeVar("R_co", covariant=True)
A_co = TypeVar("A_co", covariant=True)

class GaMutationSupport(Generic[R_co,A_co], metaclass=ABCMeta):

    @abstractmethod
    def copy(self):
        """
        Copy the current object

        :return:  new instance with the same properties
        :rtype: :class:`GaMutationSupport`
        """
        raise NotImplementedError
        
    @abstractmethod
    def mutation(self, problem:Problem, solution:Solution[R_co,A_co],  
                optimizer:PopulationBasedMetaheuristic)->None:
        """
        GA individual mutation based on some probability

        :param `Problem` problem: problem that is solved
        :param `Solution[R_co,A_co]` solution: individual that is mutated
        :param `PopulationBasedMetaheuristic` optimizer: metaheuristic optimizer that is executed
        :return: None
        """
        raise NotImplementedError
    