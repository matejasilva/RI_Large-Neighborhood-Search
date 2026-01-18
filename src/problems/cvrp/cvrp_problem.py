from lns.basic_lns import BasicLNS
from lns.adaptive_lns import AdaptiveLNS
from enums import LNSMethod

class CVRPProblem:
    def __init__(self, nodes, demands, number_of_vehicles, capacity, depot=0):
        self.nodes = nodes
        self.demands = demands
        self.number_of_vehicles = number_of_vehicles
        self.capacity = capacity
        self.depot = depot

    def initial_solution(self):
        pass

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