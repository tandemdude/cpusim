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

from cpusim.instructions import base
from cpusim.instructions import utils

if t.TYPE_CHECKING:
    from cpusim import simulator


class Ret(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.DIRECT

    def repr(self, args: tuple[int, ...]) -> str:
        return "ret"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        raise NotImplementedError("RET is not implemented")


class Move(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"move {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        cpu.registers.set(args_.register_1, cpu.registers.get(args_.register_2))


class Load(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER_INDIRECT

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterIndirectModeArgs(*args)
        return f"load {utils.register_repr(args_.register_1)} ({utils.register_repr(args_.register_2)})"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterIndirectModeArgs(*args)

        cpu.registers.set(args_.register_1, cpu.memory.get(cpu.registers.get(args_.register_2).unsigned_value))


class Store(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER_INDIRECT

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterIndirectModeArgs(*args)
        return f"store {utils.register_repr(args_.register_1)} ({utils.register_repr(args_.register_2)})"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterIndirectModeArgs(*args)

        cpu.memory.set(cpu.registers.get(args_.register_2).unsigned_value, cpu.registers.get(args_.register_1))


class Rol(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"rol {utils.register_repr(args_.register_1)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.rol(cpu.registers.get(args_.register_1))
        cpu.registers.set(args_.register_1, result)


class Xor(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"xor {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.xor(cpu.registers.get(args_.register_1), cpu.registers.get(args_.register_2))
        cpu.registers.set(args_.register_1, result)


class Ror(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"ror {utils.register_repr(args_.register_1)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.ror(cpu.registers.get(args_.register_1))
        cpu.registers.set(args_.register_1, result)


class Add(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"add {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.add(cpu.registers.get(args_.register_1), cpu.registers.get(args_.register_2))
        cpu.registers.set(args_.register_1, result)


class Sub(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"sub {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.sub(cpu.registers.get(args_.register_1), cpu.registers.get(args_.register_2))
        cpu.registers.set(args_.register_1, result)


class And(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"and {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.and_(cpu.registers.get(args_.register_1), cpu.registers.get(args_.register_2))
        cpu.registers.set(args_.register_1, result)


class Or(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"or {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.or_(cpu.registers.get(args_.register_1), cpu.registers.get(args_.register_2))
        cpu.registers.set(args_.register_1, result)


class Asl(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"sub {utils.register_repr(args_.register_1)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        args_ = base.RegisterModeArgs(*args)

        result = cpu.alu.asl(cpu.registers.get(args_.register_1))
        cpu.registers.set(args_.register_1, result)


class Xop2(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER_INDIRECT

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterIndirectModeArgs(*args)
        return f"xop2 {utils.register_repr(args_.register_1)} ({utils.register_repr(args_.register_2)})"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        raise NotImplementedError("XOP2 is not implemented")


class Xop3(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"xop3 {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        raise NotImplementedError("XOP3 is not implemented")


class Xop4(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER_INDIRECT

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterIndirectModeArgs(*args)
        return f"xop4 {utils.register_repr(args_.register_1)} ({utils.register_repr(args_.register_2)})"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        raise NotImplementedError("XOP4 is not implemented")


class Xop5(base.Instruction):
    __slots__ = ()

    addressing_mode = base.AddressingMode.REGISTER

    def repr(self, args: tuple[int, ...]) -> str:
        args_ = base.RegisterModeArgs(*args)
        return f"xop5 {utils.register_repr(args_.register_1)} {utils.register_repr(args_.register_2)}"

    def execute(self, args: tuple[int, ...], cpu: simulator.CPU) -> None:
        raise NotImplementedError("XOP5 is not implemented")
