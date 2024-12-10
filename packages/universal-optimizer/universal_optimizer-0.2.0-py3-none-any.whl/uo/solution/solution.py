""" 
The :mod:`~uo.solution.solution` module describes the class :class:`~uo.solution.Solution`.
"""

from copy import deepcopy
from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)

from random import random, randrange, choice

from abc import ABCMeta, abstractmethod
from typing import TypeVar
from typing import Generic
from typing import Optional

from uo.problem.problem import Problem
from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.evaluation_cache_control_statistics import EvaluationCacheControlStatistics
from uo.solution.distance_calculation_cache_control_statistics import DistanceCalculationCacheControlStatistics

R_co = TypeVar("R_co", covariant=True) 
A_co = TypeVar("A_co", covariant=True)

class Solution(Generic[R_co,A_co], metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self, 
            random_seed:Optional[int], 
            fitness_value:Optional[float|int], 
            fitness_values:Optional[list[float]|tuple[float]], 
            objective_value:Optional[float|int], 
            objective_values:Optional[list[float]|tuple[float]], 
            is_feasible:bool,
            evaluation_cache_is_used:bool=False,
            evaluation_cache_max_size:Optional[int]=None,
            distance_calculation_cache_is_used:bool=False,
            distance_calculation_cache_max_size:Optional[int]=None
    )->None:
        """
        Create new Solution instance
        :param int random_seed: random seed for initialization
        :param fitness_value: fitness value of the target solution
        :type fitness_value: float 
        :param fitness_values: fitness values of the target solution
        :type fitness_values: list[float]|tuple(float) 
        :param objective_value: objective value of the target solution
        :type objective_value: float
        :param objective_values: objective values of the target solution
        :type objective_values: list[float]|tuple(float) 
        :param bool evaluation_cache_is_used: should cache be used during evaluation of the solution
        :param int evaluation_cache_max_size: maximum size of the cache used for evaluation - 0 if size is unlimited
        :param bool distance_calculation_cache_is_used: should cache be used during calculation of the distance between
        :param int distance_calculation_cache_max_size: maximum size of the cache used for distance calculation - 0 if 
        size is unlimited
        """
        if not isinstance(random_seed, Optional[int]):
                raise TypeError('Parameter \'random_seed\' must be \'int\' or \'None\'.')        
        if not isinstance(objective_value, Optional[float|int]):
                raise TypeError('Parameter \'objective_value\' must be \'float\' or \'int\' or \'None\'.')        
        if not isinstance(objective_values, Optional[list]) and not isinstance(objective_values, Optional[tuple]):
                raise TypeError('Parameter \'objective_values\' must be \'lost[float]\' or \'tuple[float]\' or \'None\'.')        
        if not isinstance(fitness_value, Optional[float|int]):
                raise TypeError('Parameter \'fitness_value\' must be \'float\' or \'int\' or \'None\'.')        
        if not isinstance(fitness_values, Optional[list]) and not isinstance(fitness_values, Optional[tuple]):
                raise TypeError('Parameter \'fitness_values\' must be \'lost[float]\' or \'tuple[float]\' or \'None\'.')        
        if not isinstance(is_feasible, bool):
                raise TypeError('Parameter \'is_feasible\' must be \'bool\'.')        
        if not isinstance(evaluation_cache_is_used, bool):
                raise TypeError('Parameter \'evaluation_cache_is_used\' must be \'bool\'.')        
        if not isinstance(evaluation_cache_max_size, int) and evaluation_cache_max_size is not None:
                raise TypeError('Parameter \'evaluation_cache_max_size\' must be \'int\' or None.')        
        if not isinstance(distance_calculation_cache_is_used, bool):
                raise TypeError('Parameter \'distance_calculation_cache_is_used\' must be \'bool\'.')        
        if not isinstance(distance_calculation_cache_max_size, int) and distance_calculation_cache_max_size is not None:
                raise TypeError('Parameter \'distance_calculation_cache_max_size\' must be \'int\' or None.')        
        if random_seed is not None and isinstance(random_seed, int) and random_seed != 0:
            self.__random_seed:int = random_seed
        else:
            self.__random_seed:int = randrange(sys.maxsize)
        self.__fitness_value:float = fitness_value
        self.__fitness_values:list[float]|tuple[float] = fitness_values
        self.__objective_value:float = objective_value
        self.__objective_values:list[float]|tuple[float] = objective_values
        self.__is_feasible:bool = is_feasible
        self.__evaluation_cache_cs:Optional[EvaluationCacheControlStatistics] = None
        if evaluation_cache_is_used:
            self.__evaluation_cache_cs:Optional[EvaluationCacheControlStatistics] = \
                EvaluationCacheControlStatistics(evaluation_cache_max_size)  
        self.__representation_distance_cache_cs:Optional[DistanceCalculationCacheControlStatistics[R_co]] = None
        if distance_calculation_cache_is_used:
            self.__representation_distance_cache_cs = \
                DistanceCalculationCacheControlStatistics[R_co](distance_calculation_cache_max_size)
        self.__representation:R_co = None

    @abstractmethod
    def copy(self):
        """
        Copy the current object

        :return:  new instance with the same properties
        :rtype: :class:`Solution`
        """
        raise NotImplementedError

    @abstractmethod
    def copy_from(self, original:'Solution')->None:
        """
        Copy all data from the original target solution
        """
        self.__evaluation_cache_cs = original.__evaluation_cache_cs
        self.__representation_distance_cache_cs = original.representation_distance_cache_cs
        self.__random_seed = original.__random_seed
        self.__fitness_value = original.__fitness_value
        self.__fitness_values = None
        if original.__fitness_values is not None:
            self.__fitness_values = original.__fitness_values.copy()
        self.__objective_value = original.__objective_value
        self.__objective_values = None
        if original.__objective_values is not None:
            self.__objective_values = original.__objective_values.copy()
        self.__is_feasible = original.__is_feasible
        r_temp = original.__representation
        if hasattr(r_temp, 'copy') and callable(getattr(r_temp, 'copy')):
            self.__representation = r_temp.copy()
        else:
            try:
                self.__representation = deepcopy(r_temp)
            except TypeError:
                self.__representation = r_temp
    
    def obtain_feasible_representation(self, problem:Problem)->R_co:
        if self.representation is None:
            raise ValueError('Solution representation should not be None.')
        return self.representation
    
    @property
    def random_seed(self)->int:
        """
        Property getter for the random seed used during metaheuristic execution
        
        :return: random seed 
        :rtype: int
        """
        return self.__random_seed

    @property
    def fitness_value(self)->float:
        """
        Property getter for fitness value of the target solution

        :return: fitness value of the target solution instance 
        :rtype: float
        """
        return self.__fitness_value

    @fitness_value.setter
    def fitness_value(self, value:float)->None:
        """
        Property setter for fitness value of the target solution

        :param value: value of the `fitness` to be set
        :type value: float
        """
        if not isinstance(value, Optional[float]) and not isinstance(value, Optional[int]):
            raise TypeError('Parameter \'fitness_value\' must have type \'float\' or \'int\'.')
        self.__fitness_value = value

    @property
    def fitness_values(self)->list[float]|tuple[float] :
        """
        Property getter for fitness values of the target solution

        :return: fitness values of the target solution instance 
        :rtype: list[float]|tuple[float] 
        """
        return self.__fitness_values

    @fitness_values.setter
    def fitness_values(self, value:list[float]|tuple[float])->None:
        """
        Property setter for fitness values of the target solution

        :param value: values of the `fitness` to be set
        :type value: list[float]|tuple[float]
        """
        if not isinstance(value, Optional[list]):
            raise TypeError('Parameter \'fitness_values\' must be list or tuple that consists of numbers.')
        self.__fitness_values = value

    @property
    def objective_value(self)->float:
        """
        Property getter for objective value of the target solution

        :return: objective value of the target solution instance 
        :rtype: float
        """
        return self.__objective_value

    @objective_value.setter
    def objective_value(self, value:float)->None:
        """
        Property setter for objective value of the target solution

        :param value: value of the `objective_value` to be set
        :type value: float
        """
        if not isinstance(value, Optional[float]) and not isinstance(value, Optional[int]):
            raise TypeError('Parameter \'objective_value\' must have type \'float\' or \'int\'.')
        self.__objective_value = value

    @property
    def objective_values(self)->list[float]|tuple[float] :
        """
        Property getter for objective values of the target solution

        :return: objective values of the target solution instance 
        :rtype: list[float]|tuple[float] 
        """
        return self.__objective_values

    @objective_values.setter
    def objective_values(self, value:list[float]|tuple[float])->None:
        """
        Property setter for objective values of the target solution

        :param value: objective values to be set
        :type value: list[float]|tuple[float]
        """
        if not isinstance(value, Optional[list]):
            raise TypeError('Parameter \'objective_values\' must be list or tuple that consists of numbers.')
        self.__objective_values = value

    @property
    def is_feasible(self)->bool:
        """
        Property getter for feasibility of the target solution

        :return: feasibility of the target solution instance 
        :rtype: bool
        """
        return self.__is_feasible

    @is_feasible.setter
    def is_feasible(self, value:bool)->None:
        """
        Property setter for feasibility of the target solution

        :param value: value to be set for the `is_feasible`
        :type value: bool
        """
        if not isinstance(value, bool):
            raise TypeError('Parameter \'is_feasible\' must have type \'bool\'.')
        self.__is_feasible = value

    @property
    def quality(self)->QualityOfSolution:
        """
        Property getter for the quality of the target solution
        
        :return: quality of the target solution, in the single-objective optimization context
        :rtype: QualityOfSolution
        """
        return QualityOfSolution(objective_value=self.objective_value, 
                    objective_values=self.objective_values,
                    fitness_value=self.fitness_value,
                    fitness_values=self.fitness_values,
                    is_feasible=self.is_feasible) 

    @property
    def evaluation_cache_cs(self)->Optional[EvaluationCacheControlStatistics]:
        """
        Property getter that returns cache for evaluation control and statistics

        :return: cache for evaluation control and statistics 
        :rtype: EvaluationCacheControlStatistics
        """
        if self.__evaluation_cache_cs is None:
            return None
        return self.__evaluation_cache_cs

    @property
    def representation_distance_cache_cs(self)->Optional[DistanceCalculationCacheControlStatistics]:
        """
        Property getter that returns cache for distance calculation control and statistics

        :return: cache for distance calculation control and statistics
        :rtype: DistanceCalculationCacheControlStatistics
        """
        if self.__representation_distance_cache_cs is None:
            return None
        return self.__representation_distance_cache_cs

    @property
    def representation(self)->R_co:
        """
        Property getter for representation of the target solution

        :return: representation of the target solution instance 
        :rtype: R_co
        """
        return self.__representation

    @representation.setter
    def representation(self, value:R_co)->None:
        """
        Property setter for representation of the target solution

        :param value: value to be set for the representation of the solution
        :type value: R_co
        """
        self.__representation = value

    @abstractmethod
    def argument(self, representation:R_co)->A_co:
        """
        Argument of the target solution

        :param representation: internal representation of the solution
        :type representation: R_co
        :return: argument of the solution 
        :rtype: A_co
        """
        raise NotImplementedError

    def is_better(self, other:"Solution", problem: Problem)->Optional[bool]:
        """
        Checks if this solution is better than the other, with respect to problem that is optimized

        :param Solution other: other solution
        :param Problem problem: problem to be solved
        :return: `True` if first is better, `False` if first is worse, `None` if quality of both 
                solutions are equal
        :rtype: bool
        """
        if problem.is_multi_objective is None:
            raise ValueError('Field \'is_multi_objective\' must not be None.')
        if not problem.is_multi_objective:
            fit1:Optional[float] = self.fitness_value;
            fit2:Optional[float] = other.fitness_value;
            # with fitness is better than without fitness
            if fit1 is None:
                if fit2 is not None:
                    return False
                else:
                    return None
            elif fit2 is None:
                return True
            # if better, return true
            if fit1 > fit2:
                return True
            # if same fitness, return None
            if fit1 == fit2:
                return None
            # otherwise, return false
            return False
        else:
            raise RuntimeError('Comparison between solutions for multi objective optimization is not currently supported.')
        
    def string_representation(self)->str:
        """
        String representation of the target solution

        :param representation: internal representation of the solution
        :type representation: R_co
        :return: string representation of the solution 
        :rtype: str
        """
        if(self.representation is None):
            return "None"
        return str(self.argument(self.representation))

    @abstractmethod
    def init_random(self, problem:Problem)->None:
        """
        Random initialization of the solution

        :param problem: problem which is solved by solution
        :type problem: `Problem`
        """
        raise NotImplementedError

    @abstractmethod
    def native_representation(self, representation_str:str)->R_co:
        """
        Obtain native representation from solution code of the `Solution` instance

        :param str representation_str: solution's representation as string (e.g. solution code)
        :return: solution's native representation 
        :rtype: R_co
        """
        raise NotImplementedError

    @abstractmethod
    def init_random(self, problem:Problem)->None:
        """
        Random initialization of the solution

        :param `Problem` problem: problem which is solved by solution
        """
        raise NotImplementedError

    @abstractmethod
    def init_from(self, representation:R_co, problem:Problem)->None:
        """
        Initialization of the solution, by setting its native representation 

        :param R_co representation: representation that will be ste to solution
        :param `Problem` problem: problem which is solved by solution
        """
        raise NotImplementedError

    @abstractmethod
    def calculate_quality_directly(self, representation:R_co, problem:Problem) -> QualityOfSolution:
        """
        Fitness calculation of the target solution

        :param R_co representation: native representation of the solution for which objective value, fitness and feasibility are calculated
        :param Problem problem: problem that is solved
        :return: objective value, fitness value and feasibility of the solution instance 
        :rtype: `QualityOfSolution`
        """
        raise NotImplementedError

    def calculate_quality(self, problem:Problem) -> QualityOfSolution:
        """
        Calculate fitness, objective and feasibility of the solution, with optional cache consultation

        :param Problem problem: problem that is solved
        :return: objective value, fitness value and feasibility of the solution instance 
        :rtype: `QualityOfSolution`
        """
        eccs:Optional[EvaluationCacheControlStatistics] = self.evaluation_cache_cs 
        if eccs is not None:
            eccs.increment_cache_request_count()
            rep:str = self.string_representation()
            if rep in eccs.cache:
                eccs.increment_cache_hit_count()
                return eccs.cache[rep]
            qos:QualityOfSolution = self.calculate_quality_directly(self.representation, problem)
            if len(eccs.cache) >= eccs.max_cache_size and len(eccs.cache)>0:
                # removing random
                code:str = choice(eccs.cache.keys())
                del eccs.cache[code]
            eccs.cache[rep] = qos
            return qos
        else:
            qos:QualityOfSolution = self.calculate_quality_directly(
                    self.representation, problem)
            return qos

    def evaluate(self, problem:Problem)->None:
        """
        Evaluate current target solution

        :param Problem problem: problem that is solved
        """        
        qos:QualityOfSolution = self.calculate_quality(problem)
        self.objective_value = qos.objective_value;
        self.fitness_value = qos.fitness_value;
        self.is_feasible = qos.is_feasible;

    @abstractmethod
    def representation_distance_directly(self, representation_1:R_co, representation_2:R_co)->float:
        """
        Directly calculate distance between two solutions determined by its native representations

        :param `R_co` representation_1: native representation for the first solution
        :param `R_co` representation_2: native representation for the second solution
        :return: distance 
        :rtype: float
        """
        raise NotImplementedError

    def representation_distance(self, representation_1:R_co, representation_2:R_co)->float:
        """
        Calculate distance between two native representations, with optional cache consultation

        :param `R_co` representation_1: native representation for the first solution
        :param `R_co` representation_2: native representation for the second solution
        :return: distance 
        :rtype: float
        """
        rdcs:Optional[DistanceCalculationCacheControlStatistics[R_co]] = self.representation_distance_cache_cs
        if rdcs is not None:
            rdcs.increment_cache_request_count()
            pair:(R_co,R_co) = (representation_1, representation_2)
            if pair in rdcs.cache:
                rdcs.increment_cache_hit_count()
                return rdcs.cache[pair]
            ret:float = self.representation_distance_directly(representation_1, representation_2)
            if len(rdcs.cache) >= rdcs.max_cache_size and len(rdcs.cache)>0:
                # removing random
                code:(R_co,R_co) = choice(rdcs.cache.keys())
                del rdcs.cache[code]
            rdcs.cache[pair] = ret
            return ret
        else:
            ret:float = self.representation_distance_directly(representation_1, representation_2)
            return ret

    def string_rep(self, delimiter:str, indentation:int=0, indentation_symbol:str='', group_start:str ='{', 
        group_end:str ='}')->str:
        """
        String representation of the target solution instance

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
        s += group_start + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol     
        s += 'fitness_value=' + str(self.fitness_value) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol     
        s += 'objective_value=' + str(self.objective_value) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol     
        s += 'is_feasible=' + str(self.is_feasible) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol     
        s += 'representation()=' + str(self.representation) + delimiter
        for _ in range(0, indentation):
            s += indentation_symbol     
        if self.evaluation_cache_cs is not None: 
            s += 'evaluation_cache_cs=' + self.evaluation_cache_cs.string_rep(
                    delimiter, indentation+1, indentation_symbol, '{', '}') 
        else:
            s += 'evaluation_cache_cs=' + 'None'
        for _ in range(0, indentation):
            s += indentation_symbol  
        if self.representation_distance_cache_cs is not None: 
            s += 'representation_distance_cache_cs=' + self.representation_distance_cache_cs.string_rep(
                    delimiter, indentation + 1, indentation_symbol, '{', '}') + delimiter
        else:
            s += 'representation_distance_cache_cs=' + 'None'
        for _ in range(0, indentation):
            s += indentation_symbol  
        s += group_end 
        return s

    @abstractmethod
    def __str__(self)->str:
        """
        String representation of the target solution instance

        :return: string representation of the target solution instance
        :rtype: str
        """
        return self.string_rep('|')

    @abstractmethod
    def __repr__(self)->str:
        """
        Representation of the target solution instance

        :return: string representation of the target solution instance
        :rtype: str
        """
        return self.string_rep('\n')

    @abstractmethod
    def __format__(self, spec:str)->str:
        """
        Formatted the target solution instance

        :param spec: str -- format specification
        :return: formatted target solution instance
        :rtype: str
        """
        return self.string_rep('|')

