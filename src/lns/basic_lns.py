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