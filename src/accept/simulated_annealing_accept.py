import random
import math

class SimulatedAnnealingAccept:
    def __init__(self, T0 = 1000, a = 0.095, Tmin = 1e-6):
        self.T = T0
        self.a = a
        self.Tmin = Tmin

    def __call__(self, new, old):
        new_cost = new.cost
        old_cost = old.cost
        
        if new_cost < old_cost:
            return True
        
        if self.T <= self.Tmin:
            return False
        
        prob = math.exp(-(new_cost - old_cost) / self.T)
        self.T *= self.a

        
        return random.random() < prob