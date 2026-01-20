import math
import random

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