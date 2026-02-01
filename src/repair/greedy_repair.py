from utils.repair import get_insert_positions

class GreedyRepair:

    def __init__(self):
        pass

    def __call__(self, solution):
        removed = solution.removed_customers.copy()

        for customer in removed:
            insertion_costs = get_insert_positions(solution, customer)

            if insertion_costs:
                _, route_id, pos = min(insertion_costs, key=lambda x: x[0])
                solution.routes[route_id].insert(pos, customer)
            else:
                solution.routes.append([customer])

        solution.removed_customers = []
        solution.cost = solution.evaluate()

        return solution