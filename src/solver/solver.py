import tsplib95
import os
from destroy.random_destroy import RandomDestroy
from destroy.worst_destroy import WorstDestroy
from destroy.related_destroy import RelatedDestroy
from destroy.worst_route_destroy import WorstRouteDestroy
from repair.greedy_repair import GreedyRepair
from repair.regret_repair import RegretRepair
from accept.simulated_annealing_accept import SimulatedAnnealingAccept
from enums import LNSMethod, DestroyMethod, RepairMethod
from utils.parser import parse_cvrp_problem

DESTROY_DICT = {
        DestroyMethod.RANDOM_DESTROY: RandomDestroy,
        DestroyMethod.WORST_DESTROY: WorstDestroy,
        DestroyMethod.RELATED_DESTROY: RelatedDestroy,
        DestroyMethod.WORST_ROUTE_DESTROY: WorstRouteDestroy
    }

REPAIR_DICT = {
        RepairMethod.GREEDY_REPAIR: GreedyRepair,
        RepairMethod.REGRET_REPAIR: RegretRepair
    }

class Solver:
    
    def __init__(self, filepath: str, algorithm: LNSMethod, repair_methods=None, destroy_methods=None, iterations=1000):
        self.filepath = filepath
        self.algorithm = algorithm
        self.iterations = iterations
        self.repair_methods = repair_methods
        self.destroy_methods = destroy_methods
        self.cvrp_problem = self.load_problem()

    def load_problem(self):
        problem = tsplib95.load(self.filepath)
        return parse_cvrp_problem(problem, os.path.basename(self.filepath))
    
    def extract_selected_methods(self):
        destroy_instances = []
        repair_instances = []

        if self.algorithm == LNSMethod.BASIC:
            destroy_instances.append(DESTROY_DICT[self.destroy_methods[0]]())
            repair_instances.append(REPAIR_DICT[self.repair_methods[0]]())
        elif self.algorithm == LNSMethod.ADAPTIVE:
            destroy_instances = [DESTROY_DICT[method]() for method in self.destroy_methods]
            repair_instances = [REPAIR_DICT[method]() for method in self.repair_methods]
        else:
            raise ValueError("Nepodržan algoritam LNS.", self.algorithm)

        return destroy_instances, repair_instances
    
    def solve(self):
        destroy_methods, repair_methods = self.extract_selected_methods()

        best_solution = self.cvrp_problem.solve(
            algorithm=self.algorithm,
            accept=SimulatedAnnealingAccept(),
            destroy_methods=destroy_methods,
            repair_methods=repair_methods,
            max_iterations=self.iterations
        )
       
        best_solution.plot()
        return best_solution