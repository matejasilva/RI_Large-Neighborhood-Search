import tsplib95
from utils.helpers import parse_cvrp_problem

def main():

    problem = tsplib95.load("instances/cvrp/Set A/examples/A-n32-k5.vrp")
    cvrp_problem = parse_cvrp_problem(problem)
    print(cvrp_problem)

if __name__ == "__main__":
    main()