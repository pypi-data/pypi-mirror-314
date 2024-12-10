""" 
..  _py_function_one_variable_max_problem:

"""
import sys
from pathlib import Path
directory = Path(__file__).resolve()
sys.path.append(directory.parent)
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent)
sys.path.append(directory.parent.parent.parent.parent.parent)

from typing import NamedTuple

from uo.utils.logger import logger

from uo.problem.problem import Problem

MaxFunctionOneVariableMaxProblemElements = NamedTuple('MaxFunctionOneVariableMaxProblemElements', 
            [('expression',str), 
            ('domain_low',float), 
            ('domain_high',float)]
        )

class MaxFunctionOneVariableMaxProblem(Problem):
    
    def __init__(self, expression:str, domain_low:float, domain_high:float)->None:
        if expression is None or expression=="":
            raise ValueError("Parameter \'expression\' should not be empty.")
        if not isinstance(domain_low, int | float):
            raise TypeError("Parameter \'domain_low\' should be \'int\' or \'float\'.")
        if not isinstance(domain_high, int | float):
            raise TypeError("Parameter \'domain_high\' should be \'int\' or \'float\'.")
        super().__init__(name="MaxFunctionOneVariableMaxProblem", is_minimization=False, is_multi_objective=False)
        self.__expression:str = expression
        self.__domain_low:float = domain_low
        self.__domain_high:float = domain_high

    def copy(self):
        obj:MaxFunctionOneVariableMaxProblem = MaxFunctionOneVariableMaxProblem(self.expression,
                                                        self.domain_low,
                                                        self.domain_high)
        return obj

    @classmethod
    def __load_from_file__(cls, file_path:str, data_format:str)->int:
        logger.debug("Load parameters: file path=" + str(file_path) 
                +  ", data format representation=" + data_format)
        if data_format=='txt':
                input_file = open(file_path, 'r')
                text_line = input_file.readline().strip()
                # skip comments
                while text_line.startswith("//") or text_line.startswith(";"):
                    text_line = input_file.readline()
                data:list[str] = text_line.split()
                if len(data)>=3:
                    return MaxFunctionOneVariableMaxProblemElements(data[0], float(data[1]), float(data[2]))
                else:
                    raise ValueError('Invalid line \'{}\' - not enough data'.format(data))        
        else:
            raise ValueError('Value for data format \'{}\' is not supported'.format(data_format))

    @classmethod
    def from_input_file(cls, input_file_path:str, input_format:str):
        """
        Additional constructor. Create new `MaxFunctionOneVariableMaxProblem` instance when input file and input format are specified

        :param str input_file_path: path of the input file with problem data
        :param str input_format: format of the input
        """
        params:MaxFunctionOneVariableMaxProblemElements = MaxFunctionOneVariableMaxProblem.__load_from_file__(input_file_path, 
                input_format)
        return cls(expression=params.expression, domain_low=params.domain_low, domain_high=params.domain_high)


    @property
    def expression(self)->str:
        return self.__expression

    @property
    def domain_low(self)->float:
        return self.__domain_low

    @property
    def domain_high(self)->float:
        return self.__domain_high

    @property
    def number_of_intervals(self)->int:
        return self.__number_of_intervals

    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
            group_end:str ='}')->str:
        if delimiter is None:
            return ''
        if indentation is None or indentation < 0:
            return ''
        if indentation_symbol is None:
            return ''
        s = delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += group_start
        s+= super().string_rep(delimiter, indentation, indentation_symbol, '', '')
        s+= delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s+= 'expression=' + self.expression
        s+= delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s+= 'domain_low=' + str(self.domain_low)
        s+= delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s+= 'domain_high=' + str(self.domain_high)
        s += group_end 
        return s

    def __str__(self)->str:
        return self.string_rep('|', 0, '', '{', '}')

    def __repr__(self)->str:
        return self.string_rep('\n', 0, '   ', '{', '}')

    def __format__(self, spec:str)->str:
        return self.string_rep('|')

