import random
import math

class RandomDestroy:
    def __init__(self, min_frac = 0.05, max_frac = 0.1):
        self.min_frac = min_frac
        self.max_frac = max_frac

    def __call__(self, solution):
        
        problem = solution.problem
        depot = problem.depot

        customers = [c for route in solution.routes
                     for c in route
                     if c != depot]
        
        if not customers:
            return solution
        
        q = math.ceil(random.uniform(self.min_frac, self.max_frac) * len(customers))

        removed = set(random.sample(customers, q))

        new_routes = []
        for route in solution.routes:
            new_routes.append([c for c in route if c not in removed])

        solution.routes = new_routes
        solution.removed_customers = list(removed)

        return solution
