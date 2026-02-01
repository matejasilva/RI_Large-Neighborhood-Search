from enum import Enum

class LNSMethod(Enum):
    BASIC = "basic"
    ADAPTIVE = "adaptive"

class DestroyMethod(Enum):
    RANDOM_DESTROY = "RandomDestroy"
    WORST_DESTROY = "WorstDestroy"
    RELATED_DESTROY = "RelatedDestroy"
    WORST_ROUTE_DESTROY = "WorstRouteDestroy"

class RepairMethod(Enum):
    GREEDY_REPAIR = "GreedyRepair"
    REGRET_REPAIR = "RegretRepair"