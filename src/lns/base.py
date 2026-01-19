from abc import ABC, abstractmethod

class BaseLNS(ABC):
    def __init__(self, accept):
        self.accept = accept

    @abstractmethod
    def destroy(self, current):
        pass

    @abstractmethod
    def repair(self, partial):
        pass

    def run(self, initial, max_iterations=100):
        current = initial.copy()
        best = current.copy()

        for _ in range(max_iterations):
            partial = self.destroy(current.copy())
            candidate = self.repair(partial)
            
            if self.accept(candidate, current):
                current = candidate
                if candidate.cost < best.cost:
                    best = candidate

        return best