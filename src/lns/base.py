from abc import ABC, abstractmethod

from destroy.random_destroy import RandomDestroy

class BaseLNS(ABC):
    def __init__(self, accept):
        self.accept = accept

    @abstractmethod
    def destroy(self, current):
        pass

    @abstractmethod
    def repair(self, partial):
        pass
    
    @abstractmethod
    def run(self, initial, max_iterations=100):
        pass