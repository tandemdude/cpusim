# Copyright (c) 2024-present tandemdude
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import typing as t

from cpusim.common.types import Int16

__all__ = ["Memory"]

ReadHookFn = t.Callable[[int], Int16]
"""
A hook function that can be called on memory read from a mapped address. Takes a single parameter,
the address written to. Must return the value to be read from that address.
"""
WriteHookFn = t.Callable[[int, Int16], None]
"""
A hook function that can be called on memory write to a mapped address. Takes two parameters,
the first is the address written to, the second is the value written.
"""


class Memory:
    __slots__ = ("_data", "_memmap_addr", "_memmap_hooks")

    def __init__(self, initial_data: list[int], max_size: int = 4096) -> None:
        data = list(initial_data)
        self._data: list[Int16] = [Int16(v) for v in data[:max_size]]
        if len(data) < max_size:
            self._data.extend([Int16(0) for _ in range(max_size - len(data))])

        self._memmap_addr: dict[int, str] = {}
        self._memmap_hooks: dict[str, tuple[ReadHookFn, WriteHookFn]] = {}

    def __repr__(self) -> str:
        return f"Memory(...{len(self._data)} entries)"

    def __getitem__(self, item: int | slice) -> Int16:
        if isinstance(item, slice):
            raise ValueError("Memory.__getitem__ does not support slicing")

        return self.get(item)

    def __setitem__(self, item: int | slice, value: t.Any) -> None:
        if isinstance(item, slice):
            raise ValueError("Memory.__setitem__ does not support slicing")
        if not isinstance(value, (Int16, int)):
            raise ValueError

        if isinstance(value, int):
            value = Int16(value)

        self.set(item, value)

    @property
    def size(self) -> int:
        return len(self._data)

    def memmap(self, id: str, addrs: t.Collection[int], on_read: ReadHookFn, on_write: WriteHookFn) -> None:
        for i in addrs:
            self._memmap_addr[i] = id

        self._memmap_hooks[id] = (on_read, on_write)

    def unmemmap(self, id: str) -> None:
        self._memmap_addr = {addr: id_ for addr, id_ in self._memmap_addr.items() if id_ != id}
        del self._memmap_hooks[id]

    def get(self, address: int) -> Int16:
        if address in self._memmap_addr:
            return self._memmap_hooks[self._memmap_addr[address]][0](address)

        if address >= len(self._data):
            raise ValueError("Address out of bounds")

        return self._data[address]

    def set(self, address: int, value: Int16) -> None:
        if address in self._memmap_addr:
            return self._memmap_hooks[self._memmap_addr[address]][1](address, value)

        if address >= len(self._data):
            raise ValueError("Address out of bounds")

        self._data[address] = value
