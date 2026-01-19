from lns.basic_lns import BasicLNS
from lns.adaptive_lns import AdaptiveLNS
from enums import LNSMethod

from .cvrp_solution import CVRPSolution

class CVRPProblem:
    def __init__(self, nodes, demands, number_of_vehicles, capacity, depot=0):
        self.nodes = nodes
        self.demands = demands
        self.number_of_vehicles = number_of_vehicles
        self.capacity = capacity
        self.depot = depot

    def initial_solution(self):
        routes = []
        vehicle_loads = []

        for _ in range(self.number_of_vehicles):
            routes.append([])
            vehicle_loads.append(0)

        vehicle_id = 0

        customers = [i for i in self.demands.keys() if i != self.depot]

        for customer in customers:
            demand = self.demands[customer]

            if vehicle_loads[vehicle_id] + demand > self.capacity:
                vehicle_id += 1

                if vehicle_id >= self.number_of_vehicles:
                    raise ValueError("Nema dovoljno vozila!")
                
            routes[vehicle_id].append(customer)
            vehicle_loads[vehicle_id] += demand


        return CVRPSolution(routes, self)


    def solve(self, initial, algorithm=LNSMethod.BASIC, **kwargs):

        if algorithm == LNSMethod.BASIC:
            lns = BasicLNS(**kwargs)
        elif algorithm == LNSMethod.ADAPTIVE:
            lns = AdaptiveLNS(**kwargs)
        else:
            raise ValueError(f"Nepoznat algoritam: {algorithm}")

        return lns.run(initial)
    
    def __str__(self):  
        return (f"CVRP Problem with {len(self.nodes)} nodes, "
                f"{self.number_of_vehicles} vehicles, "
                f"capacity {self.capacity}, depot at {self.depot}")
    
    