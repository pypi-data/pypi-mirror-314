"""Implementation of FileLike in a real FileSystem"""
import os

import aiofiles

from . import FileLike, FileLikeSystem


class OsFile(FileLike):
    """Implementation of FileLike in a real FileSystem"""

    def __init__(self, filename: str, mode: str):
        self._fn = filename
        self._mode = mode if "b" in mode else "b" + mode
        self._context = None
        self._f = None
        self._new = True
        self._content = b""

    async def __aenter__(self):
        if os.path.exists(self._fn):
            self._context = aiofiles.open(self._fn, self._mode)
            self._f = await self._context.__aenter__()
            self._new = False
        else:
            self._context = aiofiles.open(self._fn, "bw")
            self._f = await self._context.__aenter__()

        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._context and self._f:
            if self._content:
                await self._f.seek(0)
                await self._f.write(self._content)
                self._content = b""

            await self._context.__aexit__(exc_type, exc, tb)
            self._context = None
            self._f = None

    async def write(self, content: bytes):
        if not self._f:
            raise RuntimeError(f"Method used out of a context")

        self._content += content

    async def read(self, size: int = -1) -> bytes:
        if not self._f:
            raise RuntimeError(f"Method used out of a context")

        if self._new:
            raise FileNotFoundError(self._fn)

        return await self._f.read(size)


class OsFileSystem(FileLikeSystem):
    """Implementation"""

    def __init__(self, root_dir: str, template: str = "{}"):
        self._root = root_dir
        self._template = template

    def _get_full_fn(self, filename: str) -> str:
        template = self._template.format(filename)
        return f"{self._root}/{template}"

    def open(self, filename: str, mode: str = "r") -> OsFile:
        full_fn = self._get_full_fn(filename)
        os.makedirs(os.path.dirname(full_fn), exist_ok=True)
        return OsFile(full_fn, mode)

    @property
    def template(self) -> str:
        """Template to generate the full filename"""
        return self._template

    @template.setter
    def template(self, value: str):
        """Change template for locating the files"""
        self._template = value

    async def rm(self, filename: str):
        os.remove(self._get_full_fn(filename))
