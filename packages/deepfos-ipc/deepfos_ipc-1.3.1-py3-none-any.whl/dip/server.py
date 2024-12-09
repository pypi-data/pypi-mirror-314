import abc
import asyncio
import typing
import sys
from uuid import UUID

from loguru import logger

from dip.proto import Protocol, SetConnectionIdProto, read_uint32
from dip.const import IS_WINDOWS

# -----------------------------------------------------------------------------
# typing

T = typing.TypeVar('T', bound='DeepfosIPCProtocol')
Callback_T = typing.Callable[
    [UUID, str, typing.Any],
    typing.Any
]


class DeepfosIPCProtocol(asyncio.BufferedProtocol):
    if typing.TYPE_CHECKING:
        _payload_feeded: bool = False

    def __init__(self: T, callback: Callback_T = None) -> None:
        self.callback = callback
        self.transport = None
        self.id = None
        self._new_playload()

    def _new_playload(self):
        self._new_buffer(5)

    def _new_buffer(
        self,
        size: int,
        is_payload: bool = True,
        mtype: int = None
    ):
        self._mtype = mtype
        self._buf_idx = 0
        self._buf = memoryview(bytearray(size))
        self._is_payload = is_payload
        self._expect_len = size

    def abort(self):
        self._new_playload()

    def get_buffer(self, sizehint: int):
        return self._buf[self._buf_idx:]

    def buffer_updated(self, nbytes: int) -> None:
        self._buf_idx += nbytes

        if self._buf_idx != self._expect_len:
            return

        if self._is_payload:
            self._new_buffer(
                size=read_uint32(self._buf[1:5])[0],
                is_payload=False,
                mtype=self._buf[0]
            )
        else:
            try:
                self.process_message(self._buf)
            except Exception as e:
                logger.error(e)
                self.transport.write(repr(e).encode("utf8"))
                self.abort()
            else:
                self.transport.write(b"ok")
                self._new_playload()

    def connection_made(self, transport):
        self.transport = transport

    def process_message(self, data: memoryview):
        mtype = self._mtype
        proto = Protocol.dispatch(mtype)
        decoded = proto.decode_body(data)
        logger.opt(lazy=True).debug("Receive data: {data!r}", data=lambda: decoded)
        if proto is SetConnectionIdProto:
            self.id = decoded
        elif self.callback is not None:
            self.callback(self.id, chr(mtype), decoded)

    def connection_lost(self, error):
        if error:
            logger.error('SERVER ERROR: {}'.format(error))
        else:
            logger.debug('connection closed.')
        super().connection_lost(error)
        self.transport = None


class AbstractServer(abc.ABC):
    def __init__(
        self,
        callback: Callback_T = None,
        loop: asyncio.AbstractEventLoop = None,
        **kwargs
    ) -> None:
        self.callback = callback
        self.waiter = None
        self.server = None
        self.kwargs = kwargs
        self._loop = loop or asyncio.get_running_loop()

    @abc.abstractmethod
    async def _create_server(self):
        return NotImplemented

    async def start(self):
        self.server = await self._create_server()
        return self.server

    async def serve_forever(self):
        self.waiter = self._loop.create_future()
        srv = await self.start()
        async with srv:
            await srv.start_serving()
            logger.info(f'Start server {self}.')
            await self.waiter
        logger.info('Server stopped.')

    def stop(self):
        if self.waiter is not None:
            self.waiter.set_result(None)
            self.waiter = None


if IS_WINDOWS:
    class Server(AbstractServer):
        def __init__(self, port: int, *args, **kwargs):
            self._port = port
            super().__init__(*args, **kwargs)

        async def _create_server(self):
            return await self._loop.create_server(
                lambda: DeepfosIPCProtocol(self.callback),
                host='localhost',
                port=self._port,
            )

        def __repr__(self):
            return f"Server(port={self._port}, platform={sys.platform})"

else:
    class Server(AbstractServer):
        def __init__(self, sockname: str, *args, **kwargs):
            self._sockname = sockname
            super().__init__(*args, **kwargs)

        async def _create_server(self):
            return await self._loop.create_unix_server(
                lambda: DeepfosIPCProtocol(self.callback),
                self._sockname,
            )

        def __repr__(self):
            return f"Server(sockname={self._sockname}, platform={sys.platform})"
