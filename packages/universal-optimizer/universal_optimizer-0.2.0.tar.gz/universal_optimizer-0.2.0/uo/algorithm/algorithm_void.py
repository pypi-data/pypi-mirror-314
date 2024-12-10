from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)

from typing import Optional

from datetime import datetime

from uo.utils.logger import logger
from uo.algorithm.output_control import OutputControl
from uo.problem.problem import Problem
from uo.problem.problem_void_min_so import ProblemVoidMinSO
from uo.solution.solution import Solution
from uo.solution.solution_void_representation_int import SolutionVoidInt


from uo.algorithm.optimizer import Optimizer
from uo.algorithm.algorithm import Algorithm

class AlgorithmVoid(Algorithm):
    def __init__(self, 
            problem:Problem=ProblemVoidMinSO(), 
            solution_template:Solution=SolutionVoidInt(),            
            name:str="algorithm_void", 
            output_control:OutputControl=None
            )->None:
        super().__init__(name=name, 
                    output_control=output_control, 
                    problem=problem, 
                    solution_template=solution_template)

    def init(self):
        return

    def copy(self):
        pr:Optional[Problem] = None
        if self.problem is not None:
            pr = self.problem.copy()
        st:Optional[Solution] = None
        if self.solution_template is not None:
            st = self.solution_template.copy()
        oc:Optional[OutputControl] = None
        if self.output_control is not None:
            oc = self.output_control.copy()
        obj  = AlgorithmVoid(pr,
                        st,
                        self.name,
                        oc)
        return obj

    def optimize(self)->Solution:
        return None
        
    def __str__(self)->str:
        return super().__str__()

    def __repr__(self)->str:
        return super().__repr__()

    def __format__(self, spec:str)->str:
        return super().__format__(spec)

