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
from cpusim.types import Int16


class ALU:
    __slots__ = ("negative", "positive", "overflow", "carry", "zero")

    def __init__(self) -> None:
        self.negative: bool = False
        self.positive: bool = False
        self.overflow: bool = False
        self.carry: bool = False
        self.zero: bool = False

    def _set_flags(self, n1: Int16, n2: Int16 | None, result: int) -> None:
        self.carry = result > 0x7fff or result < -0x8000
        self.negative = result < 0
        self.positive = result > 0
        self.zero = result == 0

    def add(self, n1: Int16, n2: Int16) -> Int16:
        result = n1 + n2
        self._set_flags(n1, n2, result)
        return Int16(result & 0xffff)

    def sub(self, n1: Int16, n2: Int16) -> Int16:
        ...

    def and_(self, n1: Int16, n2: Int16) -> Int16:
        ...

    def rol(self, n: Int16) -> Int16:
        ...

    def xor(self, n1: Int16, n2: Int16) -> Int16:
        ...

    def or_(self, n1: Int16, n2: Int16) -> Int16:
        ...

    def ror(self, n: Int16) -> Int16:
        ...

    def asl(self, n: Int16) -> Int16:
        ...
