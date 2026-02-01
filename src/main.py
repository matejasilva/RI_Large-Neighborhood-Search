import tsplib95
from utils.parser import parse_cvrp_problem

from problems.cvrp.cvrp_problem import CVRPProblem
from problems.cvrp.cvrp_solution import CVRPSolution

from destroy.random_destroy import RandomDestroy
from destroy.worst_destroy import WorstDestroy
from destroy.related_destroy import RelatedDestroy
from destroy.worst_route_destroy import WorstRouteDestroy

from repair.greedy_repair import GreedyRepair
from repair.regret_repair import RegretRepair

from accept.simulated_annealing_accept import SimulatedAnnealingAccept
from enums import LNSMethod

def main():

    problem = tsplib95.load("instances/cvrp/Set A/examples/A-n44-k6.vrp")
    cvrp_problem = parse_cvrp_problem(problem)
    print("Problem loaded.")
    print(cvrp_problem)
    problem = CVRPProblem(
        cvrp_problem.nodes,
        cvrp_problem.demands,
        cvrp_problem.number_of_vehicles,
        cvrp_problem.capacity,
        cvrp_problem.depot
    )

    # for _ in range(10):
    #     best_solution = problem.solve(algorithm=LNSMethod.BASIC,
    #                                 accept=SimulatedAnnealingAccept(),
    #                                 destroy=RandomDestroy(),
    #                                 repair=RegretRepair(),
    #                                 max_iterations=10000)


    # print("Solution found:")
    # print(best_solution)
    # best_solution.plot()

    best_solution = problem.solve(
    algorithm=LNSMethod.ADAPTIVE,
    accept=SimulatedAnnealingAccept(),
    destroy_methods=[
        RandomDestroy(),
        WorstDestroy(),
        RelatedDestroy(),
        WorstRouteDestroy()
    ],
    repair_methods=[
        GreedyRepair(),
        RegretRepair()
    ],
    max_iterations=100000
)
    
    print("Solution found:")
    print(best_solution)
    best_solution.plot()
    

if __name__ == "__main__":
    main()