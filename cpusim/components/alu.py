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
    __slots__ = ("carry", "negative", "overflow", "positive", "zero")

    def __init__(self) -> None:
        self.negative: bool = False
        self.positive: bool = False
        self.overflow: bool = False
        self.carry: bool = False
        self.zero: bool = False

    def _set_basic_flags(self, result: Int16) -> None:
        self.negative = result.signed_value < 0
        self.positive = result.signed_value > 0
        self.zero = result.signed_value == 0

    def add(self, n1: Int16, n2: Int16) -> Int16:
        result = n1 + n2

        self._set_basic_flags(result)
        self.carry = result.carry
        self.overflow = result.overflow

        return result

    def sub(self, n1: Int16, n2: Int16) -> Int16:
        result = n1 - n2

        self._set_basic_flags(result)
        self.carry = False
        self.overflow = result.overflow

        return result

    def and_(self, n1: Int16, n2: Int16) -> Int16:
        result = Int16(n1.unsigned_value & n2.unsigned_value)

        self._set_basic_flags(result)
        self.carry = self.overflow = False

        return result

    def rol(self, n: Int16) -> Int16:
        result = Int16((n.unsigned_value << 1) | (n.unsigned_value >> 15))

        self._set_basic_flags(result)
        self.carry = self.overflow = False

        return result

    def xor(self, n1: Int16, n2: Int16) -> Int16:
        result = Int16(n1.unsigned_value ^ n2.unsigned_value)

        self._set_basic_flags(result)
        self.carry = self.overflow = False

        return result

    def or_(self, n1: Int16, n2: Int16) -> Int16:
        result = Int16(n1.unsigned_value | n2.unsigned_value)

        self._set_basic_flags(result)
        self.carry = self.overflow = False

        return result

    def ror(self, n: Int16) -> Int16:
        result = Int16((n.unsigned_value >> 1) | ((n.unsigned_value & 0x1) << 15))

        self._set_basic_flags(result)
        self.carry = self.overflow = False

        return result

    def asl(self, n: Int16) -> Int16:
        result = Int16((n.unsigned_value << 1) & 0xFFFE)

        self._set_basic_flags(result)
        self.carry = self.overflow = False

        return result
