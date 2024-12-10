from typing import Self, Protocol


class FileLike(Protocol):
    """Interface to be implemented by storage systems like a asynchronous file"""

    async def __aenter__(self) -> Self:
        """Context manager"""
        ...

    async def __aexit__(self, exc_type, exc, tb):
        """Context manager"""
        ...

    async def read(self, size: int = -1) -> bytes:
        """Read content of file"""
        ...

    async def write(self, b: bytes):
        """Write bytes to the file"""
        ...

    # async def close(self):
    #     """Close file"""

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
    # seek
    # seekable
    # tell
    # truncate
    # writable
    # write
    # writelines
    # readline
    # readlines


class FileLikeSystem(Protocol):
    def open(self, filename: str, mode: str) -> FileLike:
        """Create a FileLike ready to be used"""
        ...

    @property
    def template(self) -> str:
        """Template to generate full filenames"""
        ...

    @template.setter
    def template(self, value: str):
        """The template should be set by the client"""
        ...

    async def rm(self, filename: str):
        """Remove file-like object"""
        ...

    async def ls(self, pattern: str):
        """List all filenames of system with simple pattern (* and ?)"""
        ...


def match(p: str, t: str):
    # If the pattern is empty, the text must also be empty
    print(p, t)
    if not p:
        return not t

    # If the pattern starts with '*'
    if p[0] == "*":
        # Match zero characters or consume one character and continue
        return match(p[1:], t) or (t and match(p, t[1:]))

    # If the pattern starts with '?', match one character
    if p[0] == "?":
        return t and match(p[1:], t[1:])

    # Match the current character and continue
    return t and p[0] == t[0] and match(p[1:], t[1:])
