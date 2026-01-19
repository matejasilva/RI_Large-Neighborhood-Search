import math

class GreedyRepair:

    def __init__(self):
        pass

    def __call__(self, solution):
        problem = solution.problem
        depot = problem.depot

        if not hasattr(solution, "removed_customers"):
            return solution

        removed = solution.removed_customers.copy()

        while removed:
            best_cost = float("inf")
            best_customer = None
            best_route_id = None
            best_position = None

            for customer in removed:
                demand = problem.demands[customer]

                for r_id, route in enumerate(solution.routes):
                    route_demand = sum(problem.demands[c] for c in route if c != depot)
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

                        real_pos = pos - 1

                        if delta < best_cost:
                            best_cost = delta
                            best_customer = customer
                            best_route_id = r_id
                            best_position = real_pos

            if best_customer is None:
                raise ValueError("Kupac ne moze biti ubacen")
            
            solution.routes[best_route_id].insert(best_position, best_customer)
            removed.remove(best_customer)

        solution.removed_customers = []
        solution.cost = solution.evaluate()

        return solution