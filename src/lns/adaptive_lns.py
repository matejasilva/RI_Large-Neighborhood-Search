from lns.base import BaseLNS
import random

class AdaptiveLNS(BaseLNS):
    def __init__(self, accept, destroy_methods, repair_methods, reaction_factor = 0.2, scores = (5, 3, 1, 0)):
        super().__init__(accept)

        self.destroy_methods = destroy_methods
        self.repair_methods = repair_methods

        self.destroy_weights = [1.0 for i in range (len(destroy_methods))]
        self.repair_weights = [1.0 for i in range (len(repair_methods))]

        self.reaction_factor = reaction_factor
        self.scores = scores

    def destroy(self, current):
        return super().destroy(current)
    
    def repair(self, partial):
        return super().repair(partial)
    
    def roulette_wheel(self, methods, weights):
        total = sum(weights)
        probs = [w / total for w in weights]
        idx = random.choices(range(len(methods)), probs)[0]
        return idx, methods[idx]
    
    def update_weights(self, score):
        if score is None:
            return 
        
        d = self.last_destroy_id
        r = self.last_repair_id

        f = self.reaction_factor

        self.destroy_weights[d] = ((1 - f) * self.destroy_weights[d] + f * score)

        self.repair_weights[r] = ((1 - f) * self.repair_weights[r] + f * score)

    def run(self, initial, max_iterations=100):
        current = initial.copy()
        best = current.copy()

        for _ in range(max_iterations):

            destroy_id, destroy = self.roulette_wheel(self.destroy_methods, self.destroy_weights)

            repair_id, repair = self.roulette_wheel(self.repair_methods, self.repair_weights)

            self.last_destroy_id = destroy_id
            self.last_repair_id = repair_id

            partial = destroy(current.copy())
            candidate = repair(partial)

            if candidate.cost < best.cost:
                score = self.scores[0]   # ω1
                best = candidate.copy()
                current = candidate

            elif candidate.cost < current.cost:
                score = self.scores[1]   # ω2
                current = candidate

            elif self.accept(candidate, current):
                score = self.scores[2]   # ω3
                current = candidate

            else:
                score = self.scores[3]   # ω4

            self.update_weights(score)

        return best