from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)

from random import random
from random import randrange
from datetime import datetime
from io import TextIOWrapper 

from uo.utils.logger import logger

from typing import Optional

from uo.problem.problem import Problem
from uo.problem.problem_void_min_so import ProblemVoidMinSO
from uo.solution.solution import Solution
from uo.solution.solution_void_representation_int import SolutionVoidInt

from uo.algorithm.output_control import OutputControl
from uo.algorithm.metaheuristic.finish_control import FinishControl
from uo.algorithm.metaheuristic.additional_statistics_control import AdditionalStatisticsControl

from uo.algorithm.metaheuristic.single_solution_metaheuristic import SingleSolutionMetaheuristic

class SingleSolutionMetaheuristicVoid(SingleSolutionMetaheuristic):
    def __init__(self, 
            finish_control:FinishControl,
            problem:Problem=ProblemVoidMinSO(),
            solution_template:Optional[Solution]=SolutionVoidInt(),   
            name:str='ss_metaheuristic_void', 
            output_control:Optional[OutputControl]=None, 
            random_seed:Optional[int]=None, 
            additional_statistics_control:Optional[AdditionalStatisticsControl]=None
    )->None:
        super().__init__(
                finish_control=finish_control,
                problem=problem,
                solution_template=solution_template,
                name=name, 
                output_control=output_control, 
                random_seed=random_seed,
                additional_statistics_control=additional_statistics_control
        )

    def init(self):
        return
    
    def copy(self):
        fc:Optional[FinishControl] = None
        if self.finish_control is not None:
            fc = self.finish_control.copy()
        pr:Optional[Problem] = None
        if self.problem is not None:
            pr = self.problem.copy()
        st:Optional[Solution] = None
        if self.solution_template is not None:
            st = self.solution_template.copy()
        oc:Optional[OutputControl] = None
        if self.output_control is not None:
            oc = self.output_control.copy()
        asc:Optional[AdditionalStatisticsControl] = None
        if self.additional_statistics_control is not None:
            asc = self.additional_statistics_control.copy()
        obj = SingleSolutionMetaheuristicVoid(fc,
                        pr,
                        st,
                        self.name,
                        oc,
                        self.random_seed,
                        asc)
        return obj
    
    def main_loop_iteration(self)->None:
        return

    def __str__(self)->str:
        return super().__str__()

    def __repr__(self)->str:
        return super().__repr__()

    def __format__(self, spec:str)->str:
        return super().__format__(spec)

