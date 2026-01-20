import random
import math

class WorstDestroy:
    def __init__(self, min_frac = 0.05, max_frac = 0.1, randomize = True):
        self.min_frac = min_frac
        self.max_frac = max_frac
        self.randomize = randomize

    def __call__(self, solution):
        
        problem = solution.problem
        depot = problem.depot

        customers = []
        for route in solution.routes:
            customers.extend(route)

        q = math.ceil(random.uniform(self.min_frac, self.max_frac) * len(customers))

        cost_decreases = []

        for route in solution.routes:
            for i, customer in enumerate(route):
                prev_node = depot if i == 0 else route[i - 1]
                next_node = depot if i == len(route) - 1 else route[i + 1]

                cost_before = (solution.distance(prev_node, customer) +
                               solution.distance(customer, next_node))
                cost_after = solution.distance(prev_node, next_node)

                cost_decrease = cost_before - cost_after
                cost_decreases.append((customer, cost_decrease))

        cost_decreases.sort(reverse=True, key=lambda x: x[1])
        removed = []

        for _ in range(q):
            if not cost_decreases:
                break
            if self.randomize:
                idx = int(pow(random.random(), 2) * len(cost_decreases))
            else:
                idx = 0
            customer, _ = cost_decreases.pop(idx)
            removed.append(customer)

        new_routes = []
        for route in solution.routes:
            new_routes.append([c for c in route if c not in removed])

        solution.routes = new_routes
        solution.removed_customers = removed

        return solution