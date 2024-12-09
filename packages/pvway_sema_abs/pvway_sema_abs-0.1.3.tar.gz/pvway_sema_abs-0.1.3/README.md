![logo](logo.png)

# SemaphoreService abstractions for python by pvWay

This pip brings the abstraction interfaces for several semaphore service flavors

## Interfaces and enums

### SemaphoreStatusEun

This enum enumerates the different possible statuses of a semaphore when trying to acquire it

* **Acquired**: (success status) the semaphore was acquired
* **ReleasedInTheMeanTime**: the semaphore was locked by someone else but when getting more info it finally appeared released.
* **OwnedBySomeoneElse**: another process currently owns the semaphore. Other processes will have to wait until the semaphore will be released by the owner process.
* **ForcedReleased**: the semaphore was locked by another process that seems not being responding for a while. As such, the release of the semaphore was forced.

```python
from enum import Enum

class SemaphoreStatusEnu(Enum):
    ACQUIRED = 1
    RELEASE_IN_THE_MEAN_TIME = 2
    OWNED_BY_SOMEONE_ELSE = 3
    FORCED_RELEASE = 4
```
### SemaphoreInfo

Small object that holds some useful information about the semaphore 

```python
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
```

### SemaphoreService
```python
import asyncio
from datetime import timedelta
from typing import Protocol, Callable, Optional, TypeVar

from src.pvway_sema_abs import semaphore_info


class SemaphoreService(Protocol):
    async def acquire_semaphore_async(
            self,
            name: str,
            owner: str,
            timeout: timedelta) -> semaphore_info:
        """
        tries to acquire a semaphore
        :param name: the (unique) same of the semaphore
        :param owner: the name of the process that tries to acquire the semaphore
        :param timeout: The estimated time out timespan that the lock will stay active (if not refreshed).
            If the semaphore is locked longer than the timeout period it will be forced release
            by any other process trying to acquire the semaphore
        :return:semaphore_info
        """
        pass

    async def touch_semaphore_async(
            self,
            name: str) -> None:
        """
        extends the validity of a given semaphore
        :param name: the unique name of the semaphore
        :return: none
        """
        pass

    async def release_semaphore_async(
            self,
            name: str) -> None:
        """
        Free a given semaphore so that another process can now acquire it
        :param name: the unique name of the semaphore
        :return: none
        """
        pass

    async def get_semaphore_async(
            self,
            name: str) -> semaphore_info:
        """
        return the semaphore info for a given semaphore name
        :param name: the unique name of the semaphore
        :return: semaphore_info
        """
        pass

    T = TypeVar('T')

    async def isolate_work_async(
            self,
            semaphore_name: str,
            owner: str,
            timeout: timedelta,
            work_async: Callable[[], asyncio.Future[T]],
            notify: Optional[Callable[[str], None]] = None,
            sleep_between_attempts: timedelta = timedelta(seconds=15)) -> T:
        """
        :param semaphore_name: The name of the semaphore to be used for synchronizing access.
        :param owner: The identifier for the entity attempting to gain access to the semaphore.
        :param timeout: The duration to wait for acquiring the semaphore before giving up.
        :param work_async: An asynchronous callable that performs the work requiring isolated access.
        :param notify: An optional callable to be invoked with status notifications, typically used for logging or alerts.
        :param sleep_between_attempts: The duration to sleep between attempts to acquire the semaphore when it is unavailable.
        :return: The result of the work executed within the isolated context.
        """
        pass
```

Happy coding
