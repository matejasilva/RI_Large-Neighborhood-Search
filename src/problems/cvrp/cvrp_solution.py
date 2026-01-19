import math
from copy import deepcopy

class CVRPSolution:
    def __init__(self, routes, problem):
        self.routes = routes
        self.problem = problem
        self.removed_customers = []
        self.cost = self.evaluate()

    def copy(self):
        new_routes = [route[:] for route in self.routes]
        s = CVRPSolution(new_routes, self.problem)
        s.removed_customers = self.removed_customers[:]
        return s
    
    def evaluate(self):
        total_cost = 0.0

        for route in self.routes:
            if not route:
                continue
            total_cost += self.distance(self.problem.depot, route[0])
            for i in range(len(route) - 1):
                total_cost += self.distance(route[i], route[i + 1])
            total_cost += self.distance(route[-1], self.problem.depot)

        return int(round(total_cost))
    
    def distance(self, i, j):
        xi, yi = self.problem.nodes[i]
        xj, yj = self.problem.nodes[j]

        return math.hypot(xi - xj, yi - yj)
    
    def __str__(self):
        s = ""
        for i, r in enumerate(self.routes, 1):
            customers = [n for n in r]
            s += f"Route #{i}: {' '.join(map(str, customers))}\n"
        s += f"Cost {self.cost}"
        return s