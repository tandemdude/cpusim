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
import abc
import typing as t

from cpusim.backend import components
from cpusim.backend import instruction_sets
from cpusim.common.instructions import base
from cpusim.common.instructions.v1a import primary as primary_1a
from cpusim.common.instructions.v1d import primary as primary_1d

InstructionT = t.TypeVar("InstructionT", base.Instruction1a, base.Instruction1d)


class CPU(abc.ABC, t.Generic[InstructionT]):
    __slots__ = ("ir", "memory", "pc")

    def __init__(self, mem: list[int] | None = None, max_mem: int = 4096) -> None:
        self.pc = components.IntRegister()
        self.ir = components.IntRegister()
        self.memory = components.Memory(mem or [], max_mem)

    @property
    @abc.abstractmethod
    def _unconditional_jump_instruction(self) -> type[InstructionT]: ...

    def fetch(self) -> None:
        current_instruction = self.memory.get(self.pc.value)
        self.ir.set(current_instruction.unsigned_value)

    @abc.abstractmethod
    def decode(self) -> tuple[InstructionT, tuple[int, ...]]: ...

    def execute(self, instruction: InstructionT, args: tuple[int, ...]) -> None:
        instruction.execute(args, self)  # type: ignore[reportArgumentType]

    def step(self, *, detect_halt_loop: bool = True) -> bool:
        self.fetch()
        instruction, args = self.decode()

        if (
            detect_halt_loop
            and isinstance(instruction, self._unconditional_jump_instruction)  # type: ignore[reportUnnecessaryIsInstance]
            and args[0] == self.pc.value
        ):
            return True

        self.execute(instruction, args)

        if instruction.incr_pc:
            self.pc.incr()

        return False


class CPU1a(CPU[base.Instruction1a]):
    __slots__ = (
        "acc",
        "alu",
    )

    INSTRUCTION_SET = instruction_sets.INSTRUCTION_SET_1A

    def __init__(self, mem: list[int] | None = None) -> None:
        super().__init__(mem, 256)

        self.acc = components.IntRegister()
        self.alu = components.Int8ALU()

    @property
    def _unconditional_jump_instruction(self) -> type[base.Instruction1a]:
        return primary_1a.JumpU

    def decode(self) -> tuple[base.Instruction1a, tuple[int, ...]]:
        raw_instruction = self.ir.value

        opcode = (raw_instruction >> 12) & 0xF

        instruction = self.INSTRUCTION_SET.get(opcode)
        if instruction is None:
            raise NotImplementedError(f"Unknown opcode {opcode}")

        arg = raw_instruction & 0xFF
        # immediate addressing mode args require the leading 0 for compatibility with v1d - v1a instructions
        # will ignore this value
        args = (0, arg) if instruction.addressing_mode is base.AddressingMode.IMMEDIATE else (arg,)

        return instruction, args


class CPU1d(CPU[base.Instruction1d]):
    __slots__ = (
        "alu",
        "registers",
    )

    INSTRUCTION_SET = instruction_sets.INSTRUCTION_SET_1D

    def __init__(self, mem: list[int] | None = None) -> None:
        super().__init__(mem)

        self.registers = components.Registers(8)
        self.alu = components.Int16ALU()

    @property
    def _unconditional_jump_instruction(self) -> type[base.Instruction1d]:
        return primary_1d.JumpU

    def decode(self) -> tuple[base.Instruction1d, tuple[int, ...]]:
        raw_instruction = self.ir.value

        # decode the instruction into its opcode(s)
        primary_opcode, secondary_opcode = (raw_instruction >> 12) & 0xF, raw_instruction & 0xF
        if primary_opcode < 0b1111:
            # secondary opcode is not used for the primary instruction set
            secondary_opcode = -1

        instruction = self.INSTRUCTION_SET.get((primary_opcode, secondary_opcode))
        if instruction is None:
            raise NotImplementedError(f"Unknown opcode {primary_opcode} {secondary_opcode}")

        # parse the instruction data into the instruction 'arguments'
        args: tuple[int, ...]

        match instruction.addressing_mode:
            case base.AddressingMode.REGISTER | base.AddressingMode.REGISTER_INDIRECT:
                args = ((raw_instruction & 0x0C00) >> 10, (raw_instruction & 0x0300) >> 8)  # R_sd, R_s
            case base.AddressingMode.IMMEDIATE:
                args = ((raw_instruction & 0x0C00) >> 10, raw_instruction & 0x00FF)  # R_sd, KK
            case base.AddressingMode.ABSOLUTE | base.AddressingMode.DIRECT:
                args = (raw_instruction & 0x0FFF,)  # AA
            case _:
                raise NotImplementedError("Unknown addressing mode")

        return instruction, args
