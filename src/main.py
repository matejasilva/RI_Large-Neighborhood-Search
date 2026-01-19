import tsplib95
from utils.helpers import parse_cvrp_problem

from problems.cvrp.cvrp_problem import CVRPProblem
from problems.cvrp.cvrp_solution import CVRPSolution

def main():

    problem = tsplib95.load("instances/cvrp/Set A/examples/A-n32-k5.vrp")
    cvrp_problem = parse_cvrp_problem(problem)

    problem = CVRPProblem(
        cvrp_problem.nodes, cvrp_problem.demands, 
        cvrp_problem.number_of_vehicles, 
        cvrp_problem.capacity, cvrp_problem.depot)
    
    solution = problem.initial_solution()

    print(solution)


if __name__ == "__main__":
    main()