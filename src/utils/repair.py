def get_insert_positions(solution, customer):
    problem = solution.problem
    depot = problem.depot
    demand = problem.demands[customer]

    insertion_positions = []

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

            insertion_positions.append((delta, index, pos - 1))

    return insertion_positions