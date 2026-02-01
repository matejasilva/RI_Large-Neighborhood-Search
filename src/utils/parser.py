import re
from problems.cvrp.cvrp_problem import CVRPProblem


def parse_cvrp_problem(problem):

    capacity = problem.capacity
    nodes = dict(problem.node_coords)
    demands = dict(problem.demands)
    depot = problem.depots[0]

    return CVRPProblem(nodes, demands, capacity, depot)
