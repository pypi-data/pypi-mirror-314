import sys
from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory)
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)

from dataclasses import dataclass
from datetime import datetime

import xarray as xr
from linopy import Model
from linopy import constraints

from uo.utils.logger import logger

from typing import Optional
from typing import Set
import numpy as np

from linopy.expressions import LinearExpression

from uo.problem.problem import Problem
from uo.solution.solution import Solution
from uo.solution.solution_void_representation_object import SolutionVoidObject
from uo.solution.quality_of_solution import QualityOfSolution


from uo.algorithm.optimizer import Optimizer
from uo.algorithm.output_control import OutputControl

from opt.single_objective.comb.min_set_cover_problem.min_set_cover_problem import MinSetCoverProblem

class MinSetCoverProblemIntegerLinearProgrammingSolverConstructionParameters:
    """
    Instance of the class :class:`MinSetCoverProblemIntegerLinearProgrammingSolverConstructionParameters` represents constructor parameters for set covering problem ILP solver.
    """
    def __init__(self, problem: Problem = None, output_control: Optional[OutputControl] = None)->None:
        if not isinstance(output_control, OutputControl) and output_control is not None:
            raise TypeError('Parameter \'output_control\' must have type \'OutputControl\' or be None.')
        if not isinstance(problem, Problem):
            raise TypeError('Parameter \'problem\' must have type \'Problem\'.')
        self.__problem = problem
        self.__output_control = output_control

    @property
    def output_control(self)->OutputControl:
        """
        Property getter for the output control
        
        :return: output control 
        :rtype: `OutputControl`
        """
        return self.__output_control    

    @property
    def problem(self)->Problem:
        """
        Property getter for the output control
        
        :return: problem that is solved
        :rtype: `Problem`
        """
        return self.__problem    


class MinSetCoverProblemIntegerLinearProgrammingSolution(SolutionVoidObject):
    def __init__(self, sol:'MinSetCoverProblemIntegerLinearProgrammingSolver')->None:
        super().__init__()
        self.__sol = sol

    def string_representation(self):
        return str(self.__sol)    

class MinSetCoverProblemIntegerLinearProgrammingSolver(Optimizer):

    def __init__(self, output_control:OutputControl=None,  problem:MinSetCoverProblem=None)->None:
        """
        Create new `MinSetCoverProblemIntegerLinearProgrammingSolver` instance

        :param `OutputControls` output_control: object that control output
        :param `MinSetCoverProblem` problem: problem to be solved
        """
        if not isinstance(output_control, OutputControl) and output_control is not None:
            raise TypeError('Parameter \'output_control\' must have type \'OutputControl\' or be None.')
        if not isinstance(problem, MinSetCoverProblem):
            raise TypeError('Parameter \'problem\' must have type \'MinSetCoverProblem\'.')
        super().__init__(name="MinSetCoverProblemIntegerLinearProgrammingSolver",
                problem=problem,  output_control=output_control )
        self.__model = Model()

    @classmethod
    def from_construction_tuple(cls, 
            construction_params:MinSetCoverProblemIntegerLinearProgrammingSolverConstructionParameters=None):
        """
        Additional constructor. Create new `MinSetCoverProblemIntegerLinearProgrammingSolver` instance from construction parameters

        :param `MinSetCoverProblemIntegerLinearProgrammingSolverConstructionParameters` construction_params: parameters for construction 
        """
        return cls(
            construction_params.output_control, 
            construction_params.problem)


    @property
    def model(self)->Model:
        """
        Property getter for the ILP model
        
        :return: model of the problem 
        :rtype: `Model`
        """
        return self.__model    

    def init(self)->None:
        super().init()
        self.iteration = -1
        self.evaluation = -1
        

    ### OVAJ DEO TREBA LEPO ISPRAVITI DA RADI ONO STO TREBA ZA MOJ PROBLEM!!!!!!!!
    def optimize(self)->MinSetCoverProblemIntegerLinearProgrammingSolution:
        """
        Uses ILP model in order to solve MinSetCoverProblem
        """
        self.init()
        l = []
        universe = self.problem.universe
        subsets = self.problem.subsets

        l = np.arange(self.problem.dimension)
        coords = xr.DataArray(l, dims="dim_i")


        # The field result_matrix_ij is set to 1 if element i is located in the set j
        result_matrix = np.zeros((len(universe), len(subsets)))

        for i in range(len(subsets)):
            subset = subsets[i]
            for element in subset:
                result_matrix[element][i] = 1

        x = self.model.add_variables(binary=True, coords = [coords] , name='x')


        np_coords = coords.values

        for i in range(len(universe)):
            transposed_vector = np.transpose(result_matrix[i])
            linear_expr = 0
            for i in range(len(np_coords)):
                linear_expr += transposed_vector[i] * x[i]
            #linear_expr = sum(coef * var for coef, var in zip(transposed_vector, x))
            #linear_expr = LinearExpression.dot(x, transposed_vector)
            self.model.add_constraints(linear_expr, ">=", 1)
        self.model.add_objective((x).sum(), sense="min")

        self.model.solve()
        self.execution_ended = datetime.now()
        self.write_output_values_if_needed("after_algorithm", "a_a")
        self.best_solution = MinSetCoverProblemIntegerLinearProgrammingSolution( self.model.solution.x )
        #logger.debug(self.model.solution.x)
        return self.best_solution


    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        
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
        :return: string representation of instance that controls output
        :rtype: str
        """            
        s = delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += group_start
        s = super().string_rep(delimiter, indentation, indentation_symbol, '', '')
        s += delimiter
        s += 'universe = ' + str(self.__universe)
        s += delimiter
        s += 'subsets=' + str(self.__subsets)
        s += group_end 
        print(s)
        return s

    def __str__(self)->str:
        """
        String representation of the 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        
        :return: string representation of the 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        :rtype: str
        """
        return self.string_rep('|')

    def __repr__(self)->str:
        """
        Representation of the 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        
        :return: string representation of the 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        :rtype: str
        """
        return self.string_rep('\n')

    def __format__(self, spec:str)->str:
        """
        Formatted 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        
        :param str spec: format specification
        :return: formatted 'MinSetCoverProblemIntegerLinearProgrammingSolver' instance
        :rtype: str
        """
        return self.string_rep('|')