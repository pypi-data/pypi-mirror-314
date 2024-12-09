import logging
from dataclasses import dataclass
from typing import Any

from redis import WatchError
from redis.asyncio import ConnectionPool, Redis

from . import FileLike, FileLikeSystem

logger = logging.getLogger(__name__)


@dataclass
class RedisConfig:
    protocol: str
    host: str | None = None
    username: str | None = None
    password: str | None = None
    port: int | None = None
    vhost: str | None = None
    query: str = ""

    def uri(self):
        value = f"{self.protocol}://"
        if self.username:
            value += self.username
        if self.password:
            value += f":{self.password}"

        if value[-2:] != "//":
            value += "@"

        if self.host:
            value += self.host

        if self.port:
            value += f":{self.port}"

        if self.vhost:
            value += f"/{self.vhost}"

        if self.query:
            value += f"?{self.query}"
        return value


class RedisFileLike(FileLike):
    """Implementation of FileLike using Redis Database"""

    def __init__(self, pool: ConnectionPool, path: str, mode="r"):
        self._key = path.replace("/", ":")
        self._pool = pool
        self._mode = mode

        self._context = None
        self._conn = None
        self._content = b""

        self._pipe_ctx = None
        self._pipe = None

    async def __aenter__(self):
        await self._open()
        return self

    async def _open(self):
        self._context = Redis(connection_pool=self._pool)
        self._conn = await self._context.__aenter__()
        if "w" in self._mode or "r+" in self._mode:
            self._pipe_ctx = self._conn.pipeline(transaction=True)
            self._pipe = await self._pipe_ctx.__aenter__()
            await self._pipe.watch(self._key)

    async def __aexit__(self, exc_type, exc, tb):
        try:
            if self._pipe and self._pipe_ctx:
                self._pipe.multi()
                if self._content:
                    await self._pipe.set(self._key, self._content)
                await self._pipe.execute()
                await self._pipe_ctx.__aexit__(exc_type, exc, tb)
                self._pipe = None
                self._pipe_ctx = None
                self._content = b""
        except WatchError:
            fn = self._key.replace(":", "/")
            raise BlockingIOError(f"File '{fn}' is open by other process")
        finally:
            if self._context:
                await self._context.__aexit__(exc_type, exc, tb)
            self._context = None

    async def read(self, size: int = -1) -> bytes:
        """Read bytes from the register"""
        if self._conn is None:
            raise RuntimeError('Method "read" called out of context')

        if size < 0:
            content = await self._conn.get(self._key)
            if content is None:
                raise FileNotFoundError(f"Not found {self._key} at Redis")
            return content

        return b""

    async def write(self, content: bytes):
        """Write content to redis register"""
        if self._conn is None:
            raise RuntimeError('Method "write" called out of context')

        self._content += content


class RedisFileSystem(FileLikeSystem):
    """Implement a file system to get access to FileLike objects"""

    def __init__(self, cfg: RedisConfig, template: str = "{}"):
        self._pool = ConnectionPool.from_url(
            cfg.uri(),
            health_check_interval=10,
            socket_timeout=10,
            socket_keepalive=True,
            socket_connect_timeout=10,
            retry_on_timeout=True,
        )
        self._template = template

    @property
    def template(self) -> str:
        """Template to generate the full filename"""
        return self._template

    @template.setter
    def template(self, value: str):
        """Change template for locating the files"""
        self._template = value

    def open(self, filename: str, mode: str = "r") -> RedisFileLike:
        """Return FileLike object"""
        return RedisFileLike(self._pool, self._template.format(filename), mode)

    async def rm(self, filename: str):
        async with Redis(connection_pool=self._pool) as conn:
            await conn.delete(self._template.format(filename).replace("/", ":"))

    async def close(self):
        await self._pool.disconnect()
