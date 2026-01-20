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

def prepare_destroy(solution, min_frac, max_frac):

    problem = solution.problem
    depot = problem.depot

    customers = [c for route in solution.routes
                    for c in route
                    if c != depot]
    
    if not customers:
        return solution

    q = math.ceil(random.uniform(min_frac, max_frac) * len(customers))
    return depot, customers, q