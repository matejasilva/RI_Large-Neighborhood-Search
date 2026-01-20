import random
from utils.destroy import prepare_destroy, get_new_routes

class RelatedDestroy:
    def __init__(self, min_frac = 0.05, max_frac = 0.1, alpha = 1, beta = 0.1, gamma = 5, randomize = True):
        self.min_frac = min_frac
        self.max_frac = max_frac
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.randomize = randomize

    def __call__(self, solution):
        _, customers, q = prepare_destroy(solution, self.min_frac, self.max_frac)

        customers_route = {}

        for route in solution.routes:
            for customer in route:    
                customers_route[customer] = route

        random_customer = random.choice(customers)

        removed = [random_customer]
        customers.remove(random_customer)

        while len(removed) < q and customers:
            relatedness = []

            for customer in customers:

                distance = solution.distance(random_customer, customer)
                demand_diff = abs(solution.problem.demands[random_customer] - solution.problem.demands[customer])
                if customers_route[random_customer] == customers_route[customer]:
                    same_route = -1
                else:
                    same_route = 1

                relatedness_score = (self.alpha * distance +
                                     self.beta * demand_diff +
                                     self.gamma * same_route)
                
                relatedness.append((customer, relatedness_score))

            relatedness.sort(key=lambda x: x[1])
            
            if self.randomize:
                idx = int(pow(random.random(), 2) * len(relatedness))
            else:
                idx = 0

            customer, _ = relatedness.pop(idx)
            removed.append(customer)
            customers.remove(customer)
        
        new_routes = get_new_routes(solution.routes, removed)

        solution.routes = new_routes
        solution.removed_customers = removed

        return solution



        
