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

from cpusim import parser
from cpusim import simulator
from cpusim.instructions import base


class DisArgs(t.NamedTuple):
    file: str


def decode_memory(cpu: simulator.CPU) -> str:
    # raw value, decoded instruction, decoded args
    instructions: list[tuple[int, base.Instruction, tuple[int, ...]]] = []

    cpu.pc.unlock()
    cpu.pc.set(0)
    while cpu.pc.value < len(cpu.memory._data):
        instruction, instruction_args = cpu.decode()
        instructions.append((cpu.memory.get(cpu.pc.value).unsigned_value, instruction, instruction_args))
        cpu.pc.incr()

    # format:
    # lineno | hex | decoded instruction
    decoded: list[str] = []

    n_zero_instructions = 0
    for lineno, current_instruction in enumerate(instructions, start=1):
        raw_instruction, instruction, instruction_args = current_instruction

        if raw_instruction == 0:
            n_zero_instructions += 1
            continue

        if n_zero_instructions != 0:
            # output info for how many lines were skipped due to zeros
            decoded.append(f"<- {n_zero_instructions} zeros omitted ->")
            n_zero_instructions = 0

        # we have a real instruction (or maybe a data line?)
        decoded.append(f"{lineno:04} | {raw_instruction:04x} | {instruction.repr(instruction_args)}")

    if n_zero_instructions != 0:
        decoded.append(f"<- {n_zero_instructions} zeros omitted ->")

    return "\n".join(decoded)


def run_dis(args: DisArgs) -> None:
    raw_instructions = parser.parse_dat_file(args.file)
    cpu = simulator.CPU(list(raw_instructions))

    output = [
        "|  DISASSEMBLER OUTPUT  |",
        "=========================",
        "LINE | HEX  | INSTRUCTION",
        "=========================",
        decode_memory(cpu)
    ]
    print("\n".join(output))
