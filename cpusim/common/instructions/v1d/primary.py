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
from cpusim.common.instructions import utils
from cpusim.common.types import Int16

if t.TYPE_CHECKING:
    from cpusim.backend import simulators


class Move(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"move {utils.register_repr(args_.register)} {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.ImmediateModeArgs(*args)
        cpu.registers.set(args_.register, utils.sign_extend_8_to_16_bits(args_.constant))


class Add(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"add {utils.register_repr(args_.register)} {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.ImmediateModeArgs(*args)

        result = cpu.alu.add(cpu.registers.get(args_.register), utils.sign_extend_8_to_16_bits(args_.constant))
        cpu.registers.set(args_.register, result)


class Sub(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"sub {utils.register_repr(args_.register)} {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.ImmediateModeArgs(*args)

        result = cpu.alu.sub(cpu.registers.get(args_.register), utils.sign_extend_8_to_16_bits(args_.constant))
        cpu.registers.set(args_.register, result)


class And(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"and {utils.register_repr(args_.register)} {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.ImmediateModeArgs(*args)

        # this constant is not sign extended
        result = cpu.alu.and_(cpu.registers.get(args_.register), Int16(args_.constant))
        cpu.registers.set(args_.register, result)


class Load(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"load RA {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        cpu.registers.set(0, cpu.memory.get(args_.constant))


class Store(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"store RA {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        cpu.memory.set(args_.constant, cpu.registers.get(0))


class AddM(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"addm RA {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        result = cpu.alu.add(cpu.registers.get(0), cpu.memory.get(args_.constant))
        cpu.registers.set(0, result)


class SubM(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.ABSOLUTE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.AbsoluteModeArgs(*args)
        return f"subm RA {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.AbsoluteModeArgs(*args)

        result = cpu.alu.sub(cpu.registers.get(0), cpu.memory.get(args_.constant))
        cpu.registers.set(0, result)


class JumpU(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpu {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.DirectModeArgs(*args)

        cpu.pc.set(args_.constant)


class JumpZ(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpz {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.DirectModeArgs(*args)

        if not cpu.alu.zero:
            return

        cpu.pc.set(args_.constant)


class JumpNZ(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpnz {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.DirectModeArgs(*args)

        if cpu.alu.zero:
            return

        cpu.pc.set(args_.constant)


class JumpC(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT
    incr_pc = False

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"jumpc {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.DirectModeArgs(*args)

        if not cpu.alu.carry:
            return

        cpu.pc.set(args_.constant)


class Call(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.DirectModeArgs(*args)
        return f"call {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        raise NotImplementedError("CALL is unimplemented")


class Or(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"or {utils.register_repr(args_.register)} {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        args_ = base.ImmediateModeArgs(*args)

        result = cpu.alu.or_(cpu.registers.get(args_.register), Int16(args_.constant))
        cpu.registers.set(args_.register, result)


class Xop1(base.Instruction1d):
    __slots__ = ()

    addressing_mode = base.AddressingMode.IMMEDIATE

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.ImmediateModeArgs(*args)
        return f"or {utils.register_repr(args_.register)} {hex(args_.constant)}"

    def execute(self, args: tuple[int, ...], cpu: simulators.CPU1d) -> None:
        raise NotImplementedError("XOP1 is unimplemented")
