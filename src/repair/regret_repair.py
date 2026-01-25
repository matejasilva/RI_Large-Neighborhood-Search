import math

class RegretRepair:
    
    def __init__(self):
        pass

    def __call__(self, solution):
        problem = solution.problem
        depot = problem.depot

        if not hasattr(solution, "removed_customers"):
            return solution
        
        removed = solution.removed_customers.copy()

        while removed:
            best_customer = None
            best_route_id = None
            best_position = None
            max_regret = -math.inf
            best_cost = None

            for customer in removed:
                demand = problem.demands[customer]
                insertion_costs = []

                for index, route in enumerate(solution.routes):
                    route_demand = sum(problem.demands[c] for c in route)
                    if route_demand + demand > problem.capacity:
                        continue

                    extended_route = [depot] + route + [depot]

                    for pos in range(1, len(extended_route)):
                        prev_node = extended_route[pos - 1]
                        next_node = extended_route[pos]

                        delta = (
                            solution.distance(prev_node, customer)
                            + solution.distance(customer, next_node)
                            - solution.distance(prev_node, next_node)
                        )

                        insertion_costs.append((delta, index, pos - 1))

                if len(insertion_costs) == 0:
                    continue

                insertion_costs.sort(key=lambda x: x[0])

                cost1, route_id1, position1 = insertion_costs[0]
                cost2 = insertion_costs[1][0] if len(insertion_costs) > 1 else float("inf")

                regret = cost2 - cost1

                if regret > max_regret:
                    max_regret = regret
                    best_customer = customer
                    best_route_id = route_id1
                    best_position = position1
                    best_cost = cost1

            if best_customer is None:
                raise ValueError("Kupac ne moze biti ubacen")
            
            solution.routes[best_route_id].insert(best_position, best_customer)
            removed.remove(best_customer)

        solution.removed_customers = []
        solution.cost = solution.evaluate()

        return solution


