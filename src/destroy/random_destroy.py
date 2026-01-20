import random
from utils.destroy import prepare_destroy

class RandomDestroy:
    def __init__(self, min_frac = 0.05, max_frac = 0.1):
        self.min_frac = min_frac
        self.max_frac = max_frac

    def __call__(self, solution):
        
        _, customers, q = prepare_destroy(solution, self.min_frac, self.max_frac)

        removed = set(random.sample(customers, q))

        new_routes = []
        for route in solution.routes:
            new_routes.append([c for c in route if c not in removed])

        solution.routes = new_routes
        solution.removed_customers = list(removed)

        return solution
