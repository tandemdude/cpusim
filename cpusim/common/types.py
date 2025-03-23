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
from __future__ import annotations

import abc
import typing as t

if t.TYPE_CHECKING:
    import typing_extensions as t_ex

__all__ = ["FixedWidthInt", "Int8", "Int16"]


class FixedWidthInt(abc.ABC):
    __slots__ = ("_value", "carry", "overflow")

    _MAX_VALUE: t.ClassVar[int]

    def __init__(self, value: int, *, carry: bool = False, overflow: bool = False) -> None:
        self._value = value & self._MAX_VALUE
        self.carry = carry
        self.overflow = overflow

    @property
    @abc.abstractmethod
    def signed_value(self) -> int: ...

    @property
    def unsigned_value(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(signed={self.signed_value}, unsigned={self.unsigned_value}"
            + (", carry=True" if self.carry else "")
            + (", overflow=True" if self.overflow else "")
            + ")"
        )

    def __eq__(self, other: t.Any) -> bool:
        if isinstance(other, FixedWidthInt):
            return self._value == other._value

        if isinstance(other, int):
            return self.unsigned_value == other if other >= 0 else self.signed_value == other

        return NotImplemented

    def __add__(self, other: t.Any) -> t_ex.Self:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot add {type(other)} to {self.__class__.__name__}")

        # do addition
        raw_result = self._value + other._value
        output = self.__class__(raw_result)

        # check unsigned to set carry flag
        if raw_result.bit_length() > self._MAX_VALUE.bit_length():
            output.carry = True

        # check signed to set overflow flag
        if (
            # adding two positive numbers should be positive
            (self.signed_value >= 0 and other.signed_value >= 0 and output.signed_value < 0)
            or
            # adding two negative numbers should be negative
            (self.signed_value < 0 and other.signed_value < 0 and output.signed_value >= 0)
        ):
            output.overflow = True

        return output

    def __sub__(self, other: t.Any) -> t_ex.Self:
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot subtract {type(other)} from {self.__class__.__name__}")

        # do subtraction
        raw_result = self.signed_value - other.signed_value
        output = self.__class__(raw_result)

        # check overflow flag - carry is not set on subtraction
        if (self.signed_value >= 0 and other.signed_value < 0 and output.signed_value < 0) or (
            self.signed_value < 0 and other.signed_value >= 0 and output.signed_value >= 0
        ):
            output.overflow = True

        return output


class Int8(FixedWidthInt):
    __slots__ = ()

    # ensure value fits within 8 bits
    _MAX_VALUE = 0xFF

    @property
    def signed_value(self) -> int:
        return (self._value ^ 0x80) - 0x80


class Int16(FixedWidthInt):
    __slots__ = ()

    # ensure value fits within 16 bits
    _MAX_VALUE = 0xFFFF

    @property
    def signed_value(self) -> int:
        return (self._value ^ 0x8000) - 0x8000
