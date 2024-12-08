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
import enum
import typing as t

if t.TYPE_CHECKING:
    from cpusim import simulator


class AddressingMode(enum.Enum):
    UNKNOWN = enum.auto()
    REGISTER = enum.auto()
    REGISTER_INDIRECT = enum.auto()
    IMMEDIATE = enum.auto()
    ABSOLUTE = enum.auto()
    DIRECT = enum.auto()


class RegisterModeArgs(t.NamedTuple):
    register_1: int
    register_2: int


RegisterIndirectModeArgs = RegisterModeArgs


class ImmediateModeArgs(t.NamedTuple):
    register: int
    constant: int


class DirectModeArgs(t.NamedTuple):
    constant: int


AbsoluteModeArgs = DirectModeArgs


class Instruction(abc.ABC):
    __slots__ = ()

    addressing_mode: t.ClassVar[AddressingMode] = AddressingMode.UNKNOWN
    incr_pc: t.ClassVar[bool] = True

    @abc.abstractmethod
    def repr(self, args: tuple[int, ...]) -> str: ...

    @abc.abstractmethod
    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: ...
