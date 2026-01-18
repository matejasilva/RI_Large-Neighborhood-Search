from src.lns.basic_lns import BasicLNS
from src.lns.adaptive_lns import AdaptiveLNS

class CVRPProblem:
    def __init__(self, nodes, demands, number_of_vehicles, depot=0):
        self.nodes = nodes
        self.demands = demands
        self.number_of_vehicles = number_of_vehicles
        self.depot = depot

    def initial_solution(self):
        pass

    def solve(self, initial, algorithm='basic', **kwargs):

        if algorithm == 'basic':
            lns = BasicLNS(**kwargs)
        elif algorithm == 'adaptive':
            lns = AdaptiveLNS(**kwargs)
        else:
            raise ValueError(f"Nepoznat algoritam: {algorithm}")

        return lns.run(initial)