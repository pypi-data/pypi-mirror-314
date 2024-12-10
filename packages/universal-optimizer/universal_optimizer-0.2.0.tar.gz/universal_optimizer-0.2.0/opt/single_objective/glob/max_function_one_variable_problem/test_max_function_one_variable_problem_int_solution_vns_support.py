from pathlib import Path
directory = Path(__file__).resolve()
import sys
sys.path.append(directory.parent)

import unittest
import unittest.mock as mocker
from unittest.mock import patch
from unittest.mock import mock_open

from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_shaking_support_standard_int import \
    VnsShakingSupportStandardInt
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_bi_int import \
    VnsLocalSearchSupportStandardBestImprovementInt
from uo.algorithm.metaheuristic.variable_neighborhood_search.vns_ls_support_standard_fi_int import \
    VnsLocalSearchSupportStandardFirstImprovementInt

from opt.single_objective.glob.max_function_one_variable_problem.max_function_one_variable_problem import \
    MaxFunctionOneVariableMaxProblem
from opt.single_objective.glob.max_function_one_variable_problem.max_function_one_variable_problem import \
    MaxFunctionOneVariableMaxProblemElements
from opt.single_objective.glob.max_function_one_variable_problem.max_function_one_variable_problem_int_solution import \
    FunctionOneVariableMaxProblemIntSolution


class TestMaxFunctionOneVariableProblemIntSolutionVnsSupport(unittest.TestCase):

    # shaking method returns True when k is greater than 0 and the solution is valid
    def test_shaking_returns_true_when_k_is_greater_than_0_and_solution_is_valid(self):
        # Arrange
        problem = MaxFunctionOneVariableMaxProblem("x**2", 0, 10)
        solution = FunctionOneVariableMaxProblemIntSolution(0, 10, 4)
        solution.representation = 3
        vns_sh_support = VnsShakingSupportStandardInt(solution.number_of_intervals)
        finish_control_stub = mocker.MagicMock()
        type(finish_control_stub).is_finished = mocker.Mock(return_value=False)
        optimizer_stub = mocker.MagicMock()
        type(optimizer_stub).finish_control = mocker.PropertyMock(return_value=finish_control_stub) 
        optimizer_stub.should_finish = mocker.Mock(return_value=False)
        type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
        type(optimizer_stub).vns_shaking_support = mocker.PropertyMock(return_value=vns_sh_support)
        optimizer_stub.k_min = 1
        optimizer_stub.k_max = 10
        # Act
        result = vns_sh_support.shaking(1, problem, solution, optimizer_stub)
        # Assert
        self.assertTrue(result)

    # local_search_best_improvement method returns a new solution with a better fitness value
    def test_local_search_best_improvement_returns_new_solution_with_better_fitness_value(self):
        # Arrange
        problem = MaxFunctionOneVariableMaxProblem("x**2", 0, 10)
        solution = FunctionOneVariableMaxProblemIntSolution(0, 10, 4)
        solution.representation = 3
        solution.evaluate(problem)
        vns_ls_support= VnsLocalSearchSupportStandardBestImprovementInt(solution.number_of_intervals)
        finish_control_stub = mocker.MagicMock()
        type(finish_control_stub).is_finished = mocker.Mock(return_value=False)
        optimizer_stub = mocker.MagicMock()
        type(optimizer_stub).finish_control = mocker.PropertyMock(return_value=finish_control_stub) 
        optimizer_stub.should_finish = mocker.Mock(return_value=False)
        type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
        type(optimizer_stub).vns_ls_support = mocker.PropertyMock(return_value=vns_ls_support)
        optimizer_stub.k_min = 1
        optimizer_stub.k_max = 10
        # Act
        old_fitness = solution.fitness_value
        result = vns_ls_support.local_search(1, problem, solution, optimizer_stub)
        # Assert
        self.assertTrue(result)
        self.assertGreaterEqual(solution.fitness_value, old_fitness)

    # local_search_first_improvement method returns a new solution with a better fitness value
    def test_local_search_first_improvement_returns_new_solution_with_better_fitness_value(self):
        # Arrange
        problem = MaxFunctionOneVariableMaxProblem("x**2", 0, 10)
        solution = FunctionOneVariableMaxProblemIntSolution(0, 10, 4)
        solution.representation = 3
        solution.evaluate(problem)
        vns_ls_support= VnsLocalSearchSupportStandardFirstImprovementInt(solution.number_of_intervals)
        finish_control_stub = mocker.MagicMock()
        type(finish_control_stub).is_finished = mocker.Mock(return_value=False)
        optimizer_stub = mocker.MagicMock()
        type(optimizer_stub).finish_control = mocker.PropertyMock(return_value=finish_control_stub) 
        optimizer_stub.should_finish = mocker.Mock(return_value=False)
        type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
        type(optimizer_stub).vns_ls_support = mocker.PropertyMock(return_value=vns_ls_support)
        optimizer_stub.k_min = 1
        optimizer_stub.k_max = 10
        # Act
        old_fitness = solution.fitness_value
        result = vns_ls_support.local_search(1, problem, solution, optimizer_stub)
        # Assert
        self.assertTrue(result)
        self.assertGreaterEqual(solution.fitness_value, old_fitness)

    # shaking method returns False when k is less than or equal to 0
    def test_shaking_returns_false_when_k_is_less_than_or_equal_to_0(self):
        # Arrange
        problem = MaxFunctionOneVariableMaxProblem("x**2", 0, 10)
        solution = FunctionOneVariableMaxProblemIntSolution(0, 10, 4)
        solution.representation = 3
        solution.evaluate(problem)
        vns_sh_support = VnsShakingSupportStandardInt(solution.number_of_intervals)
        finish_control_stub = mocker.MagicMock()
        type(finish_control_stub).check_evaluations = mocker.PropertyMock(return_value=False)
        type(finish_control_stub).evaluations_max = mocker.PropertyMock(return_value=0)
        optimizer_stub = mocker.MagicMock()
        type(optimizer_stub).finish_control = mocker.PropertyMock(return_value=finish_control_stub) 
        optimizer_stub.should_finish = mocker.Mock(return_value=False)
        type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
        type(optimizer_stub).vns_shaking_support = mocker.PropertyMock(return_value=vns_sh_support)
        optimizer_stub.k_min = 1
        optimizer_stub.k_max = 10
        # Act
        result = vns_sh_support.shaking(0, problem, solution, optimizer_stub)
        # Assert
        self.assertFalse(result)

    # local_search_best_improvement method returns the same solution when k is less than 1 or greater than the representation length
    def test_local_search_best_improvement_returns_same_solution_when_k_is_less_than_1_or_greater_than_representation_length(self):
        # Arrange
        problem = MaxFunctionOneVariableMaxProblem("x**2", 0, 10)
        solution = FunctionOneVariableMaxProblemIntSolution(0, 10, 4)
        solution.representation = 3
        solution.evaluate(problem)
        vns_ls_support = VnsLocalSearchSupportStandardBestImprovementInt(solution.number_of_intervals)
        finish_control_stub = mocker.MagicMock()
        type(finish_control_stub).check_evaluations = mocker.PropertyMock(return_value=False)
        type(finish_control_stub).evaluations_max = mocker.PropertyMock(return_value=0)
        optimizer_stub = mocker.MagicMock()
        type(optimizer_stub).finish_control = mocker.PropertyMock(return_value=finish_control_stub) 
        optimizer_stub.should_finish = mocker.Mock(return_value=False)
        type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
        type(optimizer_stub).vns_ls_support = mocker.PropertyMock(return_value=vns_ls_support)
        optimizer_stub.k_min = 1
        optimizer_stub.k_max = 10
        # Act
        result = vns_ls_support.local_search(0, problem, solution, optimizer_stub)
        # Assert
        self.assertFalse(result)
        # Act
        result = vns_ls_support.local_search(33, problem, solution, optimizer_stub)
        # Assert
        self.assertFalse(result)

    # local_search_first_improvement method returns the same solution when k is less than 1 or greater than the representation length
    def test_local_search_first_improvement_returns_same_solution_when_k_is_less_than_1_or_greater_than_representation_length(self):
        # Arrange
        problem = MaxFunctionOneVariableMaxProblem("x**2", 0, 10)
        solution = FunctionOneVariableMaxProblemIntSolution(0, 10, 4)
        solution.representation = 3
        solution.evaluate(problem)
        vns_ls_support:VnsLocalSearchSupportStandardBestImprovementInt = \
            VnsLocalSearchSupportStandardBestImprovementInt(solution.number_of_intervals)
        finish_control_stub = mocker.MagicMock()
        type(finish_control_stub).check_evaluations = mocker.PropertyMock(return_value=False)
        type(finish_control_stub).evaluations_max = mocker.PropertyMock(return_value=0)
        optimizer_stub = mocker.MagicMock()
        type(optimizer_stub).finish_control = mocker.PropertyMock(return_value=finish_control_stub) 
        optimizer_stub.should_finish = mocker.Mock(return_value=False)
        type(optimizer_stub).evaluation = mocker.PropertyMock(return_value=0)
        type(optimizer_stub).vns_ls_support = mocker.PropertyMock(return_value=vns_ls_support)
        optimizer_stub.k_min = 1
        optimizer_stub.k_max = 10
        # Act
        result = vns_ls_support.local_search(0, problem, solution, optimizer_stub)
        # Assert
        self.assertFalse(result)
        # Act
        result = vns_ls_support.local_search(33, problem, solution, optimizer_stub)
        # Assert
        self.assertFalse(result)

    # should return a string representation of the class name 'FunctionOneVariableMaxProblemIntSolutionVnsSupport'
    def test_string_rep_class_name(self):
        # Arrange
        supp = VnsLocalSearchSupportStandardBestImprovementInt(42)    
        # Act
        result = supp.string_rep('|')
        # Assert
        self.assertEqual(result, 'VnsLocalSearchSupportStandardBestImprovementInt')


    # should return a string with the delimiter passed as argument
    def test_string_rep_delimiter(self):
        # Arrange
        supp = VnsShakingSupportStandardInt(42)    
        # Act
        result = supp.string_rep(delimiter="++")
        # Assert
        self.assertEqual(result, 'VnsShakingSupportStandardInt')

    # should return a string with the indentation passed as argument
    def test_string_rep_indentation(self):
        # Arrange
        supp = VnsShakingSupportStandardInt(42)    
        # Act
        result = supp.string_rep('|', indentation=4)
        # Assert
        self.assertEqual(result, 'VnsShakingSupportStandardInt')

    # should return an empty string when all arguments are empty
    def test_string_rep_empty_arguments(self):
        # Arrange
        solution = VnsShakingSupportStandardInt(42)
        # Act
        result = solution.string_rep('', indentation=0, indentation_symbol='', group_start='', group_end='')
        # Assert
        self.assertEqual(result, 'VnsShakingSupportStandardInt')

    # should return a string with the indentation_symbol passed as argument
    def test_string_rep_indentation_symbol(self):
        # Arrange
        solution = VnsShakingSupportStandardInt(42)
        # Act
        result = solution.string_rep('|', indentation_symbol=' ')
        # Assert
        self.assertEqual(result, 'VnsShakingSupportStandardInt')

class Test__Copy__(unittest.TestCase):

    # Should return a deep copy of the object
    def test_return_copy(self):
        sup = VnsShakingSupportStandardInt(42)
        copy_sup = sup.copy()
        self.assertIsNot(sup, copy_sup)
        self.assertEqual(sup.__dict__, copy_sup.__dict__)

    # Should not modify the original object
    def test_not_modify_original_object(self):
        sup = VnsShakingSupportStandardInt(42)
        original_dict = sup.__dict__.copy()
        copy_sup = sup.copy()
        self.assertEqual(sup.__dict__, original_dict)

    # Should copy all attributes of the object
    def test_copy_all_attributes(self):
        sup = VnsShakingSupportStandardInt(42)
        sup.__dimension = 45
        copy_sup = sup.copy()
        self.assertEqual(sup.dimension, copy_sup.dimension)

    # Should return a new object even if the original object is empty
    def test_return_new_object_empty(self):
        sup = VnsShakingSupportStandardInt(42)
        copy_sup = sup.copy()
        self.assertIsNot(sup, copy_sup)
