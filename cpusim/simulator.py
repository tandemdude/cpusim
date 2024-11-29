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


class CPU:
    def __init__(self, mem: list[int]) -> None:
        self.pc = pc.ProgramCounter()
        self.registers = registers.Registers(8)
        self.memory = memory.Memory(mem)
        self.alu = alu.ALU()

    def step(self) -> None:
        self.pc.unlock()
        # TODO - implement control logic

        instruction = self.memory.get(self.pc.value)

        # decode the instruction into its opcode(s)
        primary_opcode, secondary_opcode = (instruction >> 12) & 0xF, instruction & 0xF

        # TODO - dictionary lookup here instead tbh

        # this instruction does not use the secondary opcode
        if primary_opcode < 0b1111:
            match primary_opcode:
                case 0b0000:
                    ...  # MOVE
                case 0b0001:
                    ...  # ADD
                case 0b0010:
                    ...  # SUB
                case 0b0011:
                    ...  # AND
                case 0b0100:
                    ...  # LOAD
                case 0b0101:
                    ...  # STORE
                case 0b0110:
                    ...  # ADDM
                case 0b0111:
                    ...  # SUBM
                case 0b1000:
                    ...  # JUMPU
                case 0b1001:
                    ...  # JUMPZ
                case 0b1010:
                    ...  # JUMPNZ
                case 0b1011:
                    ...  # JUMPC
                case 0b1100:
                    ...  # CALL
                case 0b1101:
                    ...  # OR
                case 0b1110:
                    ...  # XOP1

        # the primary opcode is 0b1111, we need to inspect the secondary opcode
        # to know which instruction this is
        match secondary_opcode:
            case 0b0000:
                ...  # RET
            case 0b0001:
                ...  # MOVE
            case 0b0010:
                ...  # LOAD
            case 0b0011:
                ...  # STORE
            case 0b0100:
                ...  # ROL
            case 0b0101:
                ...  # ROR
            case 0b0110:
                ...  # ADD
            case 0b0111:
                ...  # SUB
            case 0b1000:
                ...  # AND
            case 0b1001:
                ...  # OR
            case 0b1010:
                ...  # XOR
            case 0b1011:
                ...  # ASL
            case 0b1100:
                ...  # XOP2
            case 0b1101:
                ...  # XOP3
            case 0b1110:
                ...  # XOP4
            case 0b1111:
                ...  # XOP5

        self.pc.incr()
        self.pc.lock()
