from utils.repair import get_insert_positions

class GreedyRepair:

    def __init__(self):
        pass

    def __call__(self, solution):

        removed = solution.removed_customers.copy()

        while removed:
            best = None

            for customer in removed:
                insertion_costs = get_insert_positions(solution, customer)

                if not insertion_costs:
                    continue

                delta, route_id, pos = min(insertion_costs, key=lambda x: x[0])

                if best is None or delta < best[0]:
                    best = (delta, customer, route_id, pos)

            if best is None:
                customer = removed[0]
                solution.routes.append([customer])
                removed.remove(customer)
                solution.cost = solution.evaluate()
                continue               
            
            _, best_customer, best_route_id, best_position = best
            solution.routes[best_route_id].insert(best_position, best_customer)
            removed.remove(best_customer)

        solution.removed_customers = []
        solution.cost = solution.evaluate()

        return solution