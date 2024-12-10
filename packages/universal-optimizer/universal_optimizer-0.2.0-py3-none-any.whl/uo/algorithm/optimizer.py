""" 
The :mod:`~uo.algorithm.optimizer` module describes the class :class:`~uo.algorithm.Optimizer`.
"""

from io import TextIOWrapper
from pathlib import Path
from typing import Optional
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)

from datetime import datetime

from abc import ABCMeta, abstractmethod

from typing import Optional

from uo.utils.logger import logger
from uo.algorithm.output_control import OutputControl
from uo.problem.problem import Problem
from uo.solution.solution import Solution

    
class Optimizer(metaclass=ABCMeta):
    """
    This class describes Optimizer
    """

    @abstractmethod
    def __init__(self, 
                problem:Problem, 
                name:str, 
                output_control:Optional[OutputControl]
    )->None:
        """
        Create new `Optimizer` instance

        :param str name: name of the optimizer
        :param `Optional[OutputControl]` output_control: structure that controls output
        :param `Problem` problem: problem to be solved
        """
        if not isinstance(problem, Problem):
                raise TypeError('Parameter \'problem\' must be \'Problem\'.')
        if not isinstance(name, str):
                raise TypeError('Parameter \'name\' must be \'str\'.')
        if not isinstance(output_control, OutputControl) and output_control is not None:
                raise TypeError('Parameter \'output_control\' must be \'OutputControl\' or None.')
        self.__problem:Problem = problem
        self.__name:str = name
        self.__output_control:Optional[OutputControl] = output_control
        self.__execution_started:Optional[datetime] = None
        self.__execution_ended:Optional[datetime] = None
        self.__best_solution:Optional[Solution] = None
        self.__time_when_best_found:Optional[float] = None


    @abstractmethod
    def copy(self):
        """
        Copy the current optimizer

        :return:  new `Optimizer` instance with the same properties
        :rtype: :class:`uo.algorithm.Optimizer`
        """
        raise NotImplementedError

    @property
    def name(self)->str:
        """
        Property getter for the name of the optimizer
        
        :return: name of the algorithm instance 
        :rtype: str
        """
        return self.__name

    @property
    def problem(self)->Problem:
        """
        Property getter for the target problem to be solved
        
        :return Problem: target problem to be solved 
        """
        return self.__problem

    @property
    def execution_started(self)->datetime:
        """
        Property getter for time when execution started
        
        :return datetime: time when execution started 
        """
        return self.__execution_started

    @execution_started.setter
    def execution_started(self, value:datetime)->None:
        """
        Property setter for time when execution started

        :param datetime value: time when execution started
        """
        if not isinstance(value, datetime):
            raise TypeError('Parameter \'execution_started\' must have type \'datetime\'.')
        self.__execution_started = value

    @property
    def execution_ended(self)->datetime:
        """
        Property getter for time when execution ended
        
        :return datetime: time when execution ended 
        """
        return self.__execution_ended

    @execution_ended.setter
    def execution_ended(self, value:datetime)->None:
        """
        Property setter for time when execution ended
        
        :param datetime value: time when execution ended
        """
        if not isinstance(value, datetime):
            raise TypeError('Parameter \'execution_ended\' must have type \'datetime\'.')
        self.__execution_ended = value

    @property
    def time_when_best_found(self)->Optional[float]:
        """
        Property getter for the time when best found
        
        :return: name of the algorithm instance 
        :rtype: Optional[float]
        """
        return self.__time_when_best_found

    @property
    def best_solution(self)->Solution:
        """
        Property getter for the best solution obtained during metaheuristic execution
        
        :return: best solution so far 
        :rtype: Solution
        """
        return self.__best_solution

    @best_solution.setter
    def best_solution(self, value:Solution)->None:
        """
        Property setter for the best solution so far
        
        :param Solution value: best solution so far
        """
        if not isinstance(value, Solution):
            raise TypeError('Parameter \'best_solution\' must have type \'Solution\'.')
        self.__best_solution = value.copy()
        self.__time_when_best_found = (datetime.now() - self.execution_started).total_seconds()

    @property
    def output_control(self)->Optional[OutputControl]:
        """
        Property getter for the output control of the executing algorithm
        
        :return: output control of the executing algorithm
        :rtype: `Optional[OutputControl]`
        """
        return self.__output_control

    @output_control.setter
    def output_control(self, value:Optional[OutputControl])->None:
        """
        Property setter for the output control of the executing algorithm
        
        :param int value: `Optional[OutputControl]`
        """
        if not isinstance(value, OutputControl) and value is not None:
            raise TypeError('Parameter \'output_control\' must have type \'OutputControl\' or None.')
        self.__output_control = value

    def determine_fields_val(self, fields_def:list[str], fields_val:list[str])->list[str]:
        """
        Determines fields values upon fields definition and old values 

        :param list[str] fields_def: list of field definitions
        :param list[str] fields_val: list of old field values
        :return: list of new field values
        :rtype: list[str]
        """ 
        for i in range(len(fields_def)):
            f_def = fields_def[i]
            old_val = fields_val[i]
            if f_def != "" and old_val == "XXX":
                s_data = "XXX"
                if f_def == "best_solution.fitness_value":
                    s_data = str(self.best_solution.fitness_value)
                elif f_def == "best_solution.fitness_values":
                    s_data = str(self.best_solution.fitness_values)
                elif f_def == "best_solution.objective_value":
                    s_data = str(self.best_solution.objective_value)
                elif f_def == "best_solution.objective_values":
                    s_data = str(self.best_solution.objective_values)
                elif f_def == "best_solution.is_feasible":
                    s_data = str(self.best_solution.is_feasible)
                elif f_def == "best_solution.string_representation()":
                    s_data = str(self.best_solution.string_representation())
                elif f_def == "execution_started":
                    s_data = str(self.execution_started)
                elif f_def == "execution_ended":
                    s_data = str(self.execution_ended)
                elif f_def == "time_when_best_found":
                    s_data = str(self.time_when_best_found)
                else:
                    try:
                        data = eval(f_def)
                        s_data:str = str(data)
                    except BaseException as e:
                        s_data:str = 'XXX'
                        logger.debug(e)
                fields_val[i] = s_data
        return fields_val

    def write_output_headers_if_needed(self)->None:
        """
        Write headers(with field names) to output file, if necessary 
        """            
        if self.output_control is not None:
            output:TextIOWrapper = self.output_control.output_file
            if output is None:
                return
            f_hs:list[str] = self.output_control.fields_headings
            line:str = ''
            for f_h in f_hs:
                output.write(f_h)
                line += f_h
                output.write('\t')
                line += '\t'
            output.write('\n')
            logger.debug(line)

    def write_output_values_if_needed(self, step_name:str, step_name_value:str):
        """
        Write data(with field values) to output file, if necessary 

        :param str step_name: name of the step when data should be written to output - have to be one of the following values: 'after_algorithm', 'before_algorithm', 'after_iteration', 'before_iteration', 'after_evaluation', 'before_evaluation', 'after_step_in_iteration', 'before_step_in_iteration'
        :param str step_name_value: what should be written to the output instead of step_name
        """            
        if self.output_control is None:
            return
        output:'TextIOWrapper' = self.output_control.output_file
        should_write:bool = False
        if step_name == 'after_algorithm':
            should_write = True
        elif step_name == 'before_algorithm':
            should_write = self.output_control.write_before_algorithm
        elif step_name == 'after_iteration':
            should_write = self.output_control.write_after_iteration
        elif step_name == 'before_iteration':
            should_write = self.output_control.write_before_iteration
        elif step_name == 'after_evaluation':
            should_write = self.output_control.write_after_evaluation
        elif step_name == 'before_evaluation':
            should_write = self.output_control.write_before_evaluation
        elif step_name == 'after_step_in_iteration':
            should_write = self.output_control.write_after_step_in_iteration
        elif step_name == 'before_step_in_iteration':
            should_write = self.output_control.write_before_step_in_iteration
        else:
            raise ValueError("Supplied step name '" + step_name + "' is not valid.")
        if should_write:
            line:str = ''
            fields_def:list[str] = self.output_control.fields_definitions 
            fields_val:list[str] = ['XXX'] * len(fields_def)
            fields_val = self.determine_fields_val(fields_def=fields_def, fields_val=fields_val)
            for f_val in fields_val:
                s_data:str = str(f_val)
                if s_data == "step_name":
                        s_data = step_name_value
                output.write( s_data + '\t')
                line += s_data + '\t'
            output.write('\n')
            logger.info(line)

    @abstractmethod
    def optimize(self)->Solution:
        """
        Method for optimization   
        """
        raise NotImplementedError()
    
    @abstractmethod
    def init(self)->None:
        self.execution_started = datetime.now()
    
    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the 'Algorithm' instance
        
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
        s = group_start
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += 'name=' + self.name + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += 'problem=' + self.problem.string_rep(delimiter, indentation + 1, 
                indentation_symbol, '{', '}')  + delimiter 
        if self.__output_control is not None:
            s += '__output_control=' + self.__output_control.string_rep(
                    delimiter, indentation + 1, indentation_symbol, '{', '}') + delimiter
        else:
            s += '__output_control=' + 'None' + delimiter
        s += 'execution_started=' + str(self.execution_started) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += 'execution_ended=' + str(self.execution_ended) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += 'best_solution=' + self.best_solution.string_rep(delimiter, indentation + 1, 
                indentation_symbol, group_start, group_end) + delimiter 
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += '__time_when_best_found=' + str(self.__time_when_best_found) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += group_end 
        return s

    @abstractmethod
    def __str__(self)->str:
        """
        String representation of the 'Algorithm' instance
        
        :return: string representation of the 'Algorithm' instance
        :rtype: str
        """
        return self.string_rep('|')

    @abstractmethod
    def __repr__(self)->str:
        """
        Representation of the 'Algorithm' instance
        
        :return: string representation of the 'Algorithm' instance
        :rtype: str
        """
        return self.string_rep('\n')

    @abstractmethod
    def __format__(self, spec:str)->str:
        """
        Formatted 'Algorithm' instance
        
        :param str spec: format specification
        :return: formatted 'Algorithm' instance
        :rtype: str
        """
        return self.string_rep('|')
