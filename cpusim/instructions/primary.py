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

from cpusim.instructions import base
from cpusim.instructions import utils

if t.TYPE_CHECKING:
    from cpusim import simulator


class Move(base.Instruction):
    addressing_mode = base.AddressingMode.IMMEDIATE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.ImmediateModeArgs(*args)
        cpu.registers.set(args_.register, utils.signed_extend_8_to_16_bits(args_.constant))


class Add(base.Instruction):
    addressing_mode = base.AddressingMode.IMMEDIATE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.ImmediateModeArgs(*args)

        # TODO - check if 16 bit signed operations work in python !
        new_value = cpu.registers.get(args_.register) + utils.signed_extend_8_to_16_bits(args_.constant)
        cpu.registers.set(args_.register, new_value)

        # TODO - set flags


class Sub(base.Instruction):
    addressing_mode = base.AddressingMode.IMMEDIATE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.ImmediateModeArgs(*args)

        # TODO - check if 16 bit signed operations work in python !
        new_value = cpu.registers.get(args_.register) - utils.signed_extend_8_to_16_bits(args_.constant)
        cpu.registers.set(args_.register, new_value)

        # TODO - set flags


class And(base.Instruction):
    addressing_mode = base.AddressingMode.IMMEDIATE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: pass


class Load(base.Instruction):
    addressing_mode = base.AddressingMode.ABSOLUTE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: pass


class Store(base.Instruction):
    addressing_mode = base.AddressingMode.ABSOLUTE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: pass


class AddM(base.Instruction):
    addressing_mode = base.AddressingMode.ABSOLUTE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: pass


class SubM(base.Instruction):
    addressing_mode = base.AddressingMode.ABSOLUTE

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: pass


class JumpU(base.Instruction):
    addressing_mode = base.AddressingMode.DIRECT

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.DirectModeArgs(*args)

        cpu.pc.set(args_.constant)
        cpu.pc.lock()


class JumpZ(base.Instruction):
    addressing_mode = base.AddressingMode.DIRECT

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.DirectModeArgs(*args)

        if not cpu.flags.zero:
            return

        cpu.pc.set(args_.constant)
        cpu.pc.lock()


class JumpNZ(base.Instruction):
    addressing_mode = base.AddressingMode.DIRECT

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.DirectModeArgs(*args)

        if cpu.flags.zero:
            return

        cpu.pc.set(args_.constant)
        cpu.pc.lock()


class JumpC(base.Instruction):
    addressing_mode = base.AddressingMode.DIRECT

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.DirectModeArgs(*args)

        if not cpu.flags.carry:
            return

        cpu.pc.set(args_.constant)
        cpu.pc.lock()


class Call(base.Instruction):
    addressing_mode = base.AddressingMode.DIRECT

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None: pass


class Xop1(base.Instruction):
    addressing_mode = base.AddressingMode.UNKNOWN

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        raise NotImplementedError("XOP1 is unimplemented")
