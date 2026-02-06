from .base import BaseLNS

class BasicLNS(BaseLNS):
    def __init__(self, accept, destroy, repair):
        super().__init__(accept)
        self.destroy = destroy
        self.repair = repair

    def destroy(self, current):
        return self._destroy(current)
    
    def repair(self, partial):
        return self._repair(partial)
    
    def run(self, initial, max_iterations=100, return_history = False):
        current = initial.copy()
        best = current.copy()

        history = []

        for _ in range(max_iterations):
            partial = self.destroy(current.copy())
            candidate = self.repair(partial)
            
            if self.accept(candidate, current):
                current = candidate
                if candidate.cost < best.cost:
                    best = candidate

            history.append(best.cost)

        if return_history:
            return best, history

        return best