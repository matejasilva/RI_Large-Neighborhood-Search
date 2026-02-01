import random
from lns.basic_lns import BasicLNS
from lns.adaptive_lns import AdaptiveLNS
from enums import LNSMethod

from .cvrp_solution import CVRPSolution

class CVRPProblem:
    def __init__(self, nodes, demands, capacity, depot=0, filename=None):
        self.nodes = nodes
        self.demands = demands
        self.capacity = capacity
        self.depot = depot
        self.filename = filename
        
    def initial_solution(self, max_attempts=20):
        for _ in range(max_attempts):
            routes = [[]]
            vehicle_loads = [0]
            vehicle_id = 0

            customers = [i for i in self.demands.keys() if i != self.depot]
            random.shuffle(customers)
            
            for customer in customers:
                demand = self.demands[customer]

                if vehicle_loads[vehicle_id] + demand > self.capacity:
                    vehicle_id += 1
                    routes.append([])
                    vehicle_loads.append(0)
                    
                routes[vehicle_id].append(customer)
                vehicle_loads[vehicle_id] += demand

            return CVRPSolution(routes, self)
            

        raise ValueError("Neuspelo generisanje pocetnog resenja nakon vise pokusaja.")

    def solve(self, algorithm=LNSMethod.BASIC, **kwargs):

        if algorithm == LNSMethod.BASIC:
            lns = BasicLNS(kwargs['accept'], kwargs['destroy_methods'][0], kwargs['repair_methods'][0])
        elif algorithm == LNSMethod.ADAPTIVE:
            lns = AdaptiveLNS(accept=kwargs['accept'],
            destroy_methods=kwargs['destroy_methods'],
            repair_methods=kwargs['repair_methods'],
            reaction_factor=kwargs.get('reaction_factor', 0.2),
            scores=kwargs.get('scores', (5, 3, 1, 0)))
        else:
            raise ValueError(f"Nepoznat algoritam: {algorithm}")

        return lns.run(self.initial_solution(), kwargs.get('max_iterations', 100))
    
    def __str__(self):  
        return (f"CVRP Problem with {len(self.nodes)} nodes, "
                f"capacity {self.capacity}, depot at {self.depot}")
    
    