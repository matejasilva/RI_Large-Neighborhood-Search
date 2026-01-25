import re
from problems.cvrp.cvrp_problem import CVRPProblem
import random
import math

def parse_cvrp_problem(problem):

    capacity = problem.capacity
    number_of_vehicles = extract_number_of_vehicles(problem.comment)
    nodes = dict(problem.node_coords)
    demands = dict(problem.demands)
    depot = problem.depots[0]

    return CVRPProblem(nodes, demands, number_of_vehicles, capacity, depot)

def extract_number_of_vehicles(comment):
    no_of_vehicles = re.search(r"No of trucks:\s*(\d+)", comment)
    if no_of_vehicles:
        return int(no_of_vehicles.group(1))
    return None
