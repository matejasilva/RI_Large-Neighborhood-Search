from utils.repair import get_insert_positions

class RegretRepair:
    
    def __init__(self):
        pass

    def __call__(self, solution):
        
        removed = solution.removed_customers.copy()

        while removed:
            best = None

            for customer in removed:
                insertion_costs = get_insert_positions(solution, customer)

                if len(insertion_costs) == 0:
                    continue

                insertion_costs.sort(key=lambda x: x[0])

                cost1, route_id1, position1 = insertion_costs[0]
                cost2 = insertion_costs[1][0] if len(insertion_costs) > 1 else float("inf")

                regret = cost2 - cost1

                if best is None or regret > best[0]:
                    best = (regret, customer, route_id1, position1)

            if best is None:
                raise ValueError("Kupac ne moze biti ubacen")
            
            _, best_customer, best_route_id, best_position = best
            solution.routes[best_route_id].insert(best_position, best_customer)
            removed.remove(best_customer)

        solution.removed_customers = []
        solution.cost = solution.evaluate()

        return solution


