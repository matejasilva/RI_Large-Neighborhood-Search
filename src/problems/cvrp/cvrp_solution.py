import math
from copy import deepcopy
import matplotlib.pyplot as plt

class CVRPSolution:
    def __init__(self, routes, problem):
        self.routes = routes
        self.problem = problem
        self.removed_customers = []
        self.cost = self.evaluate()
        self.previous_solution = routes

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
    
    def plot(self):
        problem = self.problem
        depot = problem.depot
        coords = problem.nodes

        plt.figure(figsize=(10, 10))

        depot_x, depot_y = coords[depot]
        plt.scatter(depot_x, depot_y, marker="s", s=120)
        plt.text(depot_x, depot_y, "Depot", fontsize=10, ha="right")

        colors = plt.cm.get_cmap("tab10", len(self.routes))

        for r_id, route in enumerate(self.routes):
            if not route:
                continue

            x = [depot_x]
            y = [depot_y]

            for c in route:
                cx, cy = coords[c]
                x.append(cx)
                y.append(cy)
                plt.text(cx, cy, str(c), fontsize=9, ha="right")

            x.append(depot_x)
            y.append(depot_y)

            plt.plot(x, y, marker="o", color=colors(r_id), label=f"Route {r_id}")

        plt.title(f"CVRP solution | cost = {self.cost}")
        plt.legend()
        plt.axis("equal")
        plt.show()