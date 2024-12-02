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
import time
import typing as t

from cpusim import parser
from cpusim import simulator
from cpusim.cmd import dis
from cpusim.instructions import utils


class CliArgs(t.NamedTuple):
    file: str
    n_steps: int
    breakpoints: list[int]
    interactive: bool


def run_cli(args: CliArgs) -> None:
    raw_instructions = parser.parse_dat_file(args.file)
    cpu = simulator.CPU(list(raw_instructions))

    elapsed_time: float
    if not args.interactive:
        # there will be no breakpoints, just run the requested number of instructions
        # and output final processor state
        before = time.perf_counter_ns()
        for _ in range(args.n_steps):
            cpu.step()
        elapsed_time = time.perf_counter_ns() - before
    else:
        ...

    microseconds = elapsed_time / 1000
    milliseconds = microseconds / 1000
    seconds = milliseconds / 1000

    final_elapsed = (
        f"{microseconds:.3f} µs"
        if milliseconds < 1
        else f"{milliseconds:.3f} ms"
        if seconds < 1
        else f"{seconds:.3f} s"
    )

    register_state_lines = [
        "| REGISTER STATE |",
        "==================",
        *(
            f"{utils.register_repr(n)} : {cpu.registers.get(n).unsigned_value:04x}".ljust(18, " ")
            for n in range(cpu.registers._register_limit)
        ),
    ]

    # 18
    if len(register_state_lines) < 7:
        register_state_lines.extend([18 * " " for _ in range(7 - len(register_state_lines))])

    register_state_lines[0] += "  | FLAG STATE |"
    register_state_lines[1] += "  =============="
    register_state_lines[2] += "  NEGATIVE : " + str(cpu.alu.negative)[0]
    register_state_lines[3] += "  POSITIVE : " + str(cpu.alu.positive)[0]
    register_state_lines[4] += "  OVERFLOW : " + str(cpu.alu.overflow)[0]
    register_state_lines[5] += "  CARRY    : " + str(cpu.alu.carry)[0]
    register_state_lines[6] += "  ZERO     : " + str(cpu.alu.zero)[0]

    output = [
        f"Instructions run : {args.n_steps}",
        f"Execution time   : {final_elapsed}",
        "",
        f"Program Counter  : {cpu.pc.value}",
        "",
        *register_state_lines,
        "",
        "|     MEMORY STATE      |",
        "=========================",
        "LINE | HEX  | INSTRUCTION",
        "=========================",
        dis.decode_memory(cpu),
    ]

    print("\n".join(output))
