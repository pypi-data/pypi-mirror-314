from datetime import timedelta, datetime
from typing import Protocol

from src.pvway_sema_abs.semaphore_status_enu import SemaphoreStatusEnu

class SemaphoreInfo(Protocol):
    @property
    def status(self) -> SemaphoreStatusEnu:
        pass

    @property
    def name(self) -> str:
        pass

    @property
    def owner(self) -> str:
        pass

    @property
    def timeout(self) -> timedelta:
        pass

    @property
    def expires_at_utc(self) -> datetime:
        pass

    @property
    def create_date_utc(self) -> datetime:
        pass

    @property
    def update_date_utc(self) -> datetime:
        pass
