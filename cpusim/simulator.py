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

from cpusim.components import alu
from cpusim.components import memory
from cpusim.components import pc
from cpusim.components import registers
from cpusim.instructions import base
from cpusim.instructions import primary
from cpusim.instructions import secondary

INSTRUCTIONS_MAP: dict[tuple[int, int], base.Instruction] = {
    (0b0000, -1): primary.Move(),
    (0b0001, -1): primary.Add(),
    (0b0010, -1): primary.Sub(),
    (0b0011, -1): primary.And(),
    (0b0100, -1): primary.Load(),
    (0b0101, -1): primary.Store(),
    (0b0110, -1): primary.AddM(),
    (0b0111, -1): primary.SubM(),
    (0b1000, -1): primary.JumpU(),
    (0b1001, -1): primary.JumpZ(),
    (0b1010, -1): primary.JumpNZ(),
    (0b1011, -1): primary.JumpC(),
    (0b1100, -1): primary.Call(),
    (0b1101, -1): primary.Or(),
    (0b1110, -1): primary.Xop1(),
    (0b1111, 0b0000): secondary.Ret(),
    (0b1111, 0b0001): secondary.Move(),
    (0b1111, 0b0010): secondary.Load(),
    (0b1111, 0b0011): secondary.Store(),
    (0b1111, 0b0100): secondary.Rol(),
    (0b1111, 0b0101): secondary.Ror(),
    (0b1111, 0b0110): secondary.Add(),
    (0b1111, 0b0111): secondary.Sub(),
    (0b1111, 0b1000): secondary.And(),
    (0b1111, 0b1001): secondary.Or(),
    (0b1111, 0b1010): secondary.Xor(),
    (0b1111, 0b1011): secondary.Asl(),
    (0b1111, 0b1100): secondary.Xop2(),
    (0b1111, 0b1101): secondary.Xop3(),
    (0b1111, 0b1110): secondary.Xop4(),
    (0b1111, 0b1111): secondary.Xop5(),
}


class CPU:
    __slots__ = ("alu", "memory", "pc", "registers")

    def __init__(self, mem: list[int]) -> None:
        self.pc = pc.ProgramCounter()
        self.registers = registers.Registers(8)
        self.memory = memory.Memory(mem)
        self.alu = alu.ALU()

    def decode(self, pc_value: int) -> tuple[base.Instruction, tuple[int, ...]]:
        raw_instruction = self.memory.get(pc_value).unsigned_value

        # decode the instruction into its opcode(s)
        primary_opcode, secondary_opcode = (raw_instruction >> 12) & 0xF, raw_instruction & 0xF
        if primary_opcode < 0b1111:
            # secondary opcode is not used for the primary instruction set
            secondary_opcode = -1

        instruction = INSTRUCTIONS_MAP.get((primary_opcode, secondary_opcode))
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

    def step(self) -> None:
        self.pc.unlock()

        instruction, args = self.decode(self.pc.value)
        instruction.execute(args, self)

        self.pc.incr()
        self.pc.lock()
