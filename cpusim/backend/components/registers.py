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
import collections

from cpusim.common.types import Int16

__all__ = ["IntRegister", "Registers"]


class IntRegister:
    __slots__ = ("_val",)

    def __init__(self) -> None:
        self._val = 0

    def __repr__(self) -> str:
        return f"IntRegister({hex(self._val)})"

    @property
    def value(self) -> int:
        return self._val

    def incr(self) -> None:
        self._val += 1

    def set(self, val: int) -> None:
        self._val = val


class Registers:
    __slots__ = (
        "_register_limit",
        "_values",
    )

    def __init__(self, register_limit: int) -> None:
        self._register_limit = register_limit
        self._values: collections.defaultdict[int, Int16] = collections.defaultdict(lambda: Int16(0))

    def __repr__(self) -> str:
        return f"Registers(...{len(self._values)} entries)"

    def get(self, idx: int) -> Int16:
        if idx >= self._register_limit:
            raise ValueError("Index out of range")

        return self._values[idx]

    def set(self, idx: int, val: Int16) -> None:
        if idx >= self._register_limit:
            raise ValueError("Index out of range")

        self._values[idx] = val
