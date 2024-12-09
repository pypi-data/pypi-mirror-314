import abc
import asyncio
import contextlib
import typing

from loguru import logger

from dip import errors
from dip.connection import Connection
from dip.const import IS_WINDOWS


class AbstractConnectionPool(abc.ABC):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        maxsize: int = 16,
        **conn_options,
    ):
        self._loop = loop or asyncio.get_running_loop()
        self._conn_opts = conn_options
        self.maxsize = maxsize
        self.queue: asyncio.Queue = asyncio.Queue(maxsize=maxsize)
        self.lock = asyncio.Lock()
        self._conns: typing.Set[Connection] = set()

    @abc.abstractmethod
    async def _new_connection(self) -> Connection:
        return NotImplemented

    async def aquire(self, timeout: int = 10) -> Connection:
        if self.queue.empty() and len(self._conns) < self.maxsize:
            async with self.lock:
                conn = await self._new_connection()
        else:
            try:
                conn = await asyncio.wait_for(self.queue.get(), timeout=timeout)
            except asyncio.TimeoutError:
                raise errors.ConnectionAquireTimeout(
                    f"Failed to aquire connection after {timeout} seconds."
                ) from None

            if conn.closed:
                self._conns.discard(conn)
                conn = await self._new_connection()
        return conn

    async def release(self, conn: Connection):
        if conn.closed:
            self._conns.discard(conn)
        else:
            await self.queue.put(conn)

    @contextlib.asynccontextmanager
    async def __call__(self) -> typing.AsyncContextManager[Connection]:
        conn = await self.aquire()
        try:
            yield conn
        finally:
            await self.release(conn)

    def dispose(self):
        for conn in self._conns:
            conn.close()

        self._conns.clear()

        q = self.queue
        for _ in range(q.qsize()):
            q.get_nowait()
            q.task_done()

    def __del__(self):
        self.dispose()


if IS_WINDOWS:
    class ConnectionPool(AbstractConnectionPool):
        def __init__(self, port: int, *args, **kwargs):
            self._port = port
            super().__init__(*args, **kwargs)

        async def _new_connection(self) -> Connection:
            logger.debug(f'Create new tcp connection to port: {self._port}')
            conn = Connection(self._port, self._loop, **self._conn_opts)
            await conn.connect()
            self._conns.add(conn)
            return conn

else:

    class ConnectionPool(AbstractConnectionPool):
        def __init__(self, sockname: str, *args, **kwargs):
            self._sockname = sockname
            super().__init__(*args, **kwargs)

        async def _new_connection(self) -> Connection:
            logger.debug(f'Create new unix connection to {self._sockname}')
            conn = Connection(self._sockname, self._loop, **self._conn_opts)
            await conn.connect()
            self._conns.add(conn)
            return conn
