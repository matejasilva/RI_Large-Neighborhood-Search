import tsplib95
from utils.helpers import parse_cvrp_problem

from problems.cvrp.cvrp_problem import CVRPProblem
from problems.cvrp.cvrp_solution import CVRPSolution

from lns.basic_lns import BasicLNS

from destroy.random_destroy import RandomDestroy
from repair.greedy_repair import GreedyRepair

from accept.simulated_annealing_accept import SimulatedAnnealingAccept

def main():

    problem = tsplib95.load("instances/cvrp/Set A/examples/A-n32-k5.vrp")
    cvrp_problem = parse_cvrp_problem(problem)

    problem = CVRPProblem(
        cvrp_problem.nodes,
        cvrp_problem.demands,
        cvrp_problem.number_of_vehicles,
        cvrp_problem.capacity,
        cvrp_problem.depot
    )

    lns = BasicLNS(SimulatedAnnealingAccept(), 
                RandomDestroy(),
                GreedyRepair())

    best_solution = lns.run(problem.initial_solution(), 1000)

    print("Best solution found:")
    print(best_solution)
    best_solution.plot()

if __name__ == "__main__":
    main()