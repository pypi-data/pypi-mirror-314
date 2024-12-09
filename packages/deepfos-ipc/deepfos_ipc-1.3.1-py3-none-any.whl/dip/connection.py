import abc
import asyncio
import typing
import uuid

from loguru import logger

from dip.const import IS_WINDOWS
from dip.proto import Protocol
from dip import errors


class ClientProtocol(asyncio.Protocol):

    def __init__(self, conn: 'Connection'):
        self.conn = conn
        self.transport = None
        self._closed = False

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if data and not self.conn.future.done():
            self.conn.future.set_result(data)
        logger.opt(lazy=True).debug(
            "Data received: {dd!r}", dd=lambda: data.decode())

    def connection_lost(self, error):
        self._closed = True
        if error:
            self.conn.future.set_exception(error)

    @property
    def closed(self):
        return self._closed


class AbstractConnection(abc.ABC):
    if typing.TYPE_CHECKING:
        transport: typing.Optional[asyncio.Transport]
        proto: typing.Optional[ClientProtocol]
        future: typing.Optional[asyncio.Future]
        id: typing.Optional[uuid.UUID]
        timeout: typing.Optional[int]

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        **options,
    ):
        self._loop = loop
        self.transport = None
        self.proto = None
        self.future = None
        self.timeout = options.get('timeout', 5)
        self.id = options.get('connection_id')

    @property
    def closed(self) -> bool:
        return (
            self.transport is None
            or self.proto is None
            or self.transport.is_closing()
            or self.proto.closed
        )

    @abc.abstractmethod
    async def _connect(self):
        return NotImplemented

    async def connect(self):
        """建立和服务端的连接"""
        if self.closed:
            self.transport, self.proto = await self._connect()
            if self.id is not None:
                r = await self.request('\x1d', self.id)
                if r != b'ok':
                    raise errors.ConnectionClosed('Failed to set id for connection.')

    async def request(self, mtype: str, message: typing.Any):
        """向服务端发送数据"""
        if self.closed:
            raise errors.ConnectionClosed("Cannot issue request after connection close.")

        self.future = self._loop.create_future()
        for data in Protocol.dispatch(ord(mtype)).encode(message):
            self.transport.write(data)
        try:
            return await asyncio.wait_for(self.future, self.timeout)
        except asyncio.TimeoutError:
            raise errors.ReadTimeout(
                f'Server failed to respond after '
                f'{self.timeout} seconds.') from None

    def close(self):
        if self.transport is not None:
            self.transport.abort()
        self.transport = None
        self.proto = None

    def __del__(self):
        self.close()


if IS_WINDOWS:
    class Connection(AbstractConnection):
        def __init__(self, port: int, *args, **kwargs):
            self._port = port
            super().__init__(*args, **kwargs)

        async def _connect(self):
            return await self._loop.create_connection(
                lambda: ClientProtocol(self),
                host='localhost',
                port=self._port,
            )

else:
    class Connection(AbstractConnection):
        def __init__(self, sockname: str, *args, **kwargs):
            self._sockname = sockname
            super().__init__(*args, **kwargs)

        async def _connect(self):
            return await self._loop.create_unix_connection(
                lambda: ClientProtocol(self),
                self._sockname
            )
