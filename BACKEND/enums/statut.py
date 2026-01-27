from enum import Enum

class OrderStatus(str, Enum):
    EN_COURS_PREPARATION = "EN_COURS_PREPARATION"
    PREPAREE = "PREPAREE"
    LIVREE = "LIVREE"
