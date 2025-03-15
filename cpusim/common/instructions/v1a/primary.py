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

import typing as t

from cpusim.common.instructions import base
from cpusim.common.types import Int8
from cpusim.common.types import Int16

if t.TYPE_CHECKING:
    from cpusim.backend import simulators


class Move(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"move {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.ImmediateModeArgs(*args)
        cpu.acc.set(args_.constant)


class Add(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"add {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.ImmediateModeArgs(*args)

        result = cpu.alu.add(Int8(cpu.acc.value), Int8(args_.constant))
        cpu.acc.set(result.unsigned_value)


class Sub(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"sub {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.ImmediateModeArgs(*args)

        result = cpu.alu.sub(Int8(cpu.acc.value), Int8(args_.constant))
        cpu.acc.set(result.unsigned_value)


class And(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"and {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.ImmediateModeArgs(*args)

        # this constant is not sign extended
        result = cpu.alu.and_(Int8(cpu.acc.value), Int8(args_.constant))
        cpu.acc.set(result.unsigned_value)


class Load(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"load {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        cpu.acc.set(Int8(cpu.memory.get(args_.constant).unsigned_value).unsigned_value)


class Store(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"store {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        cpu.memory.set(args_.constant, Int16(cpu.acc.value))


class AddM(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"addm {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        result = cpu.alu.add(Int8(cpu.acc.value), Int8(cpu.memory.get(args_.constant).unsigned_value))
        cpu.acc.set(result.unsigned_value)


class SubM(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"subm {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        result = cpu.alu.sub(Int8(cpu.acc.value), Int8(cpu.memory.get(args_.constant).unsigned_value))
        cpu.acc.set(result.unsigned_value)


class JumpU(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpu {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.DirectModeArgs(*args)

        cpu.pc.set(args_.constant)


class JumpZ(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpz {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.DirectModeArgs(*args)

        if not cpu.alu.zero:
            return

        cpu.pc.set(args_.constant)


class JumpNZ(base.Instruction1a):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpnz {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1a) -> None:
        args_ = base.DirectModeArgs(*args)

        if cpu.alu.zero:
            return

        cpu.pc.set(args_.constant)
