import asyncio
from datetime import timedelta
from typing import Protocol, Callable, Optional, TypeVar

from src.pvway_sema_abs.semaphore_info import SemaphoreInfo


class SemaphoreService(Protocol):
    async def acquire_semaphore_async(
            self,
            name: str,
            owner: str,
            timeout: timedelta) -> SemaphoreInfo:
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
            name: str) -> SemaphoreInfo:
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
