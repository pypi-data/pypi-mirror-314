from enum import Enum

class SemaphoreStatusEnu(Enum):
    ACQUIRED = 1
    RELEASE_IN_THE_MEAN_TIME = 2
    OWNED_BY_SOMEONE_ELSE = 3
    FORCED_RELEASE = 4