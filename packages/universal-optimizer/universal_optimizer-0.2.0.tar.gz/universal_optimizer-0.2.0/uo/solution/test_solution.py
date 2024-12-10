
import unittest   
import unittest.mock as mocker

from uo.problem.problem import Problem 

from uo.solution.quality_of_solution import QualityOfSolution
from uo.solution.solution import Solution 
from uo.solution.solution_void_representation_int import SolutionVoidInt

class TestSolutionProperties(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("setUpClass TestSolutionProperties\n")

    def setUp(self):       
        self.random_seed = 42
        self.fitness_value = 42.0
        self.objective_value = -42.0
        self.is_feasible = True
        self.solution = SolutionVoidInt( random_seed=self.random_seed,
                fitness_value=self.fitness_value,
                objective_value=self.objective_value,
                is_feasible= self.is_feasible, 
                evaluation_cache_is_used=True,
                distance_calculation_cache_is_used=True
        )
    
    def test_fitness_value_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.solution.fitness_value, self.fitness_value)

    def test_objective_value_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.solution.objective_value, self.objective_value)

    def test_is_feasible_should_be_equal_as_in_constructor(self):
        self.assertEqual(self.solution.is_feasible, self.is_feasible)

    def test_fitness_value_should_be_equal_as_value_set_by_property_setter(self):
        val:float = 42.1
        self.solution.fitness_value = val
        self.assertEqual(self.solution.fitness_value, val)

    def test_fitness_value_should_be_equal_as_value_set_by_property_setter_2(self):
        val:int = 11
        self.solution.fitness_value = val
        self.assertEqual(self.solution.fitness_value, val)

    def test_objective_value_should_be_equal_as_value_set_by_property_setter(self):
        val:float = 43.1
        self.solution.objective_value = val
        self.assertEqual(self.solution.objective_value, val)

    def test_is_feasible_should_be_equal_as_value_set_by_property_setter(self):
        val:bool = False
        self.solution.is_feasible = val
        self.assertEqual(self.solution.is_feasible, val)

    def test_is_feasible_should_be_equal_as_value_set_by_property_setter_2(self):
        val:bool = True
        self.solution.is_feasible = val
        self.assertEqual(self.solution.is_feasible, val)

    def test_representation_should_be_equal_as_value_set_by_property_setter(self):
        val:int = 42
        self.solution.representation =  val
        self.assertEqual(self.solution.representation, val)

    def test_representation_should_be_equal_as_value_set_by_property_setter_2(self):
        val:int = -7
        self.solution.representation =  val
        self.assertEqual(self.solution.representation, val)

    def test_evaluation_cache_cs_hit_count_should_be_zero_after_constructor(self):
        random_seed = 42
        fitness_value = 42.0
        objective_value = -42.0
        is_feasible = True
        solution = SolutionVoidInt( random_seed=random_seed,
                fitness_value=fitness_value,
                objective_value=objective_value,
                is_feasible= is_feasible, 
                evaluation_cache_is_used=True,
                distance_calculation_cache_is_used=True
        )
        self.assertEqual(solution.evaluation_cache_cs.cache_hit_count, 0)

    def test_evaluation_cache_cs__request_count_should_be_zero_after_constructor(self):
        random_seed = 42
        fitness_value = 42.0
        objective_value = -42.0
        is_feasible = True
        solution = SolutionVoidInt( random_seed=random_seed,
                fitness_value=fitness_value,
                objective_value=objective_value,
                is_feasible= is_feasible, 
                evaluation_cache_is_used=True,
                distance_calculation_cache_is_used=True
        )
        self.assertEqual(solution.evaluation_cache_cs.cache_request_count, 0)

    def test_distance_calculation_cache_hit_count_should_be_zero_after_constructor(self):
        random_seed = 42
        fitness_value = 42.0
        objective_value = -42.0
        is_feasible = True
        solution = SolutionVoidInt( random_seed=random_seed,
                fitness_value=fitness_value,
                objective_value=objective_value,
                is_feasible= is_feasible, 
                distance_calculation_cache_is_used=True
        )
        self.assertEqual(solution.representation_distance_cache_cs.cache_hit_count, 0)

    def test_distance_calculation_cache_cs__request_count_should_be_zero_after_constructor(self):
        random_seed = 42
        fitness_value = 42.0
        objective_value = -42.0
        is_feasible = True
        solution = SolutionVoidInt( random_seed=random_seed,
                fitness_value=fitness_value,
                objective_value=objective_value,
                is_feasible= is_feasible, 
                distance_calculation_cache_is_used=True
        )
        self.assertEqual(solution.representation_distance_cache_cs.cache_request_count, 0)

    def tearDown(self):
        return

    @classmethod
    def tearDownClass(cls):
        print("\ntearDownClass TestSolutionProperties")
    
if __name__ == '__main__':
    unittest.main()