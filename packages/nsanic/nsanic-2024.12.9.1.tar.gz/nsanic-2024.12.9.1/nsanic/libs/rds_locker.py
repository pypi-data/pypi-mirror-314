import asyncio

from redis.asyncio.lock import Lock


class RdsLocker(Lock):

    _watcher: asyncio.Task

    async def __waiting(self):
        while 1:
            await self.extend(self.timeout)
            await asyncio.sleep(self.timeout/3)

    def __stop_watcher(self):
        old: asyncio.Future = getattr(self, "_watcher", None)
        if old and (not old.cancelled()):
            old.cancel()

    async def acquire(self, blocking: bool = None, timeout: float = None, token: (str, bytes) = None) -> bool:
        result = await super().acquire(blocking, timeout, token)
        if result:
            self.__stop_watcher()
            self._watcher = asyncio.create_task(self.__waiting())
        return result

    async def do_release(self, expected_token: bytes) -> None:
        self.__stop_watcher()
        return await super().do_release(expected_token)

    def __del__(self) -> None:
        try:
            self.__stop_watcher()
        except Exception as err:
            _ = err
            pass
