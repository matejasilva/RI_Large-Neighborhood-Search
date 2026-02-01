import random
from utils.destroy import get_new_routes, prepare_destroy

class WorstRouteDestroy:
    def __init__(self, min_frac = 0.05, max_frac = 0.1):
        self.min_frac = min_frac
        self.max_frac = max_frac

    def __call__(self, solution):

        depot, _, q = prepare_destroy(solution, self.min_frac, self.max_frac)

        routes_costs = []

        for route in solution.routes:
            if not route:
                routes_costs.append((route, 0))
                continue

            cost = 0
            extended_route = [depot] + route + [depot]
            for i in range(len(extended_route) - 1):
                cost += solution.distance(extended_route[i], extended_route[i + 1])

            routes_costs.append((route, cost))

        routes_costs.sort(key=lambda x: x[1], reverse=True)

        D = 4.0
        r = random.random()
        idx = int((r ** D) * len(routes_costs))

        worst_route = routes_costs[idx][0]
        q= min(q, len(worst_route))
        removed = random.sample(worst_route, q)

        new_routes = get_new_routes(solution.routes, removed)
        
        solution.previous_solution = solution.routes
        solution.routes = new_routes
        solution.removed_customers = removed
        
        return solution