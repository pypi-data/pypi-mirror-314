import abc
from typing import Self



class FileLike(abc.ABC):
    """Interface to be implemented by storage systems like a asynchronous file"""

    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        """Context manager"""
        return self

    @abc.abstractmethod
    async def __aexit__(self, exc_type, exc, tb):
        """Context manager"""

    @abc.abstractmethod
    async def read(self, size: int = -1) -> bytes:
        """Read content of file"""

    @abc.abstractmethod
    async def write(self, b: bytes):
        """Write bytes to the file"""

    # @abc.abstractmethod
    # async def close(self):
    #     """Close file"""

    # @abc.abstractmethod
    # async def open(self):
    #     """Open the file"""

    # async def seekable(self) -> bool:
    #     return True

    # close
    # flush

    # isatty
    # read
    # readall
    # read1
    # readinto
    # readline
    # readlines
    # seek
    # seekable
    # tell
    # truncate
    # writable
    # write
    # writelines


class FileLikeSystem(abc.ABC):
    @abc.abstractmethod
    def open(self, filename: str, mode: str) -> FileLike:
        """Create a FileLike ready to be used"""

    @property
    @abc.abstractmethod
    def template(self) -> str:
        """Template to generate full filenames"""

    @template.setter
    @abc.abstractmethod
    def template(self, value: str):
        """The template should be set by the client"""

    @abc.abstractmethod
    async def rm(self, filename: str):
        """Remove file-like object"""
