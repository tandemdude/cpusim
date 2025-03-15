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
import re
import time
import typing as t

from cpusim_old import __version__
from cpusim_old import parser
from cpusim_old import simulator
from cpusim_old.cmd import dis
from cpusim_old.instructions import base
from cpusim_old.instructions import utils
from cpusim_old.types import Int16


class CliArgs(t.NamedTuple):
    file: str
    n_steps: int
    breakpoints: list[int]
    interactive: bool
    auto_halt: bool


INTERACTIVE_MODE_HELP_OUTPUT = "\n".join(
    [
        "Available Commands:",
        "",
        "=== Information ===",
        "help      - show this message",
        "registers - dump the register contents to terminal",
        "flags     - dump the flag states to terminal",
        "memory    - dump the memory contents to terminal",
        "exit      - exit the program and dump processor state to terminal",
        "            ALIASES: quit, stop, halt",
        "",
        "=== Debugging ===",
        "PC             - view the current value of the program counter",
        "RX             - view the contents of register RX",
        "RX = $         - set the value of register RX",
        "                 'X' should be replaced with the letter of the correct register",
        "                 '$' may be a decimal (e.g. 10), hex (e.g. 0xff), or binary value (e.g. 0b11)",
        "mem[addr]      - view the contents of memory at addr",
        "mem[addr] = $  - set the value of memory at addr",
        "                'addr' and '$' may be a decimal (e.g. 10), hex (e.g. 0xff), or binary value (e.g. 0b11)",
        "dis $          - disassemble the given value into an assembly instruction",
        "dis RX         - disassemble the value of the given register into an assembly instruction",
        "dis mem[addr]  - disassemble the value in memory at the given address into an assembly instruction",
        "",
        "=== Execution ===",
        "step           - run the next instruction and then wait for input",
        "step N         - step through N instructions and then wait for input",
        "                 'N' must be a decimal value (e.g. 10)",
        "step .         - step until the next breakpoint is hit, a halt-loop is detected (if auto-halt enabled),",
        "                 or the max number of instructions have been executed",
        "                 (the max number of instructions was set using the '-s' or '--steps' CLI flag when the program was run)",
        "break set N    - set a breakpoint at instruction N (as output by 'python -m cpusim dis <file>')",
        "                 'N' must be a decimal value (e.g. 10)",
        "                 ALIASES: bp set"
        "break set expr - set a conditional breakpoint to trigger when 'expr' evaluates to 'True'",
        "                 ALIASES: bp set" "break list     - list the current breakpoints",
        "                 ALIASES: bp list"
        "break del ID   - delete the breakpoint with the given ID (as output by 'break list')",
        "                 ALIASES: bp del" "",
        "NOTE: all commands are case-sensitive unless otherwise specified",
    ]
)

# matches a decimal number, a hexadecimal number, or a binary number
_dec_hex_bin = r"\d+|0x[0-9a-fA-F]+|0b[01]+"
# matches a register name (e.g. RA) and extracts the letter into a named capture group
_register = r"R(?P<reg_letter>[A-Z])"
# matches a memory access (e.g. mem[123]) and extracts the address into a named capture group
_memory = rf"mem\[(?P<mem_addr>{_dec_hex_bin})]"

DEBUG_REGISTER_EXPR = re.compile(rf"^{_register}\s*(?:=\s*(?P<new_val>{_dec_hex_bin}))?$")
DEBUG_MEMORY_EXPR = re.compile(rf"{_memory}\s*(?:=\s*(?P<new_val>{_dec_hex_bin}))?$")
DEBUG_DISASSEMBLE_EXPR = re.compile(rf"^dis\s+(?:(?P<literal>{_dec_hex_bin})|{_register}|{_memory})$")

EXECUTION_STEP_EXPR = re.compile(r"^step(?:\s+(?P<arg>\d+|\.))?$")
EXECUTION_BREAKPOINT_EXPR = re.compile(r"^(?:break|bp)\s*(?P<cmd>set|list|del)(?:\s*(?P<arg>.*))?$")


def number_string_to_int(number_string: str) -> int:
    if number_string.startswith("0x"):
        return int(number_string, 16)
    elif number_string.startswith("0b"):
        return int(number_string, 2)
    return int(number_string)


def run_interactive_cli(cpu: simulator.CPU, args: CliArgs) -> int:
    total_instructions_run = 0
    all_breakpoints: list[int | t.Callable[[simulator.CPU], bool] | None] = [*(args.breakpoints or [])]

    command = input(
        f"CPUSim CLI interactive mode (v{__version__})\n" "Run 'help' to see available commands\n" ">>> "
    ).strip()
    while True:
        # information commands
        if command == "help":
            print(INTERACTIVE_MODE_HELP_OUTPUT)
        elif command == "registers":
            # fmt: off
            print("\n".join([
                "| REGISTER STATE |",
                "==================",
                *(
                    f"{utils.register_repr(n)} : {cpu.registers.get(n).unsigned_value:04x}"
                    for n in range(cpu.registers._register_limit)
                ),
            ]))
            # fmt: on
        elif command == "flags":
            # fmt: off
            print("\n".join([
                "| FLAG STATE |",
                "==============",
                "NEGATIVE : " + ("ON" if cpu.alu.negative else "OFF"),
                "POSITIVE : " + ("ON" if cpu.alu.positive else "OFF"),
                "OVERFLOW : " + ("ON" if cpu.alu.overflow else "OFF"),
                "CARRY    : " + ("ON" if cpu.alu.carry else "OFF"),
                "ZERO     : " + ("ON" if cpu.alu.zero else "OFF"),
            ]))
            # fmt: on
        elif command == "memory":
            # fmt: off
            print("\n".join([
                "|     MEMORY STATE      |",
                "=========================",
                "LINE | HEX  | INSTRUCTION",
                "=========================",
                dis.decode_memory(cpu, include_pc=True),
            ]))
            # fmt: on
        elif command in ("exit", "quit", "stop", "halt"):
            print("<- exited interactive mode ->\n")
            return total_instructions_run

        # debugging commands
        elif command == "PC":
            print(f"READ -> PC : {cpu.pc.value} (hex {cpu.pc.value:04x})")
        elif match := DEBUG_REGISTER_EXPR.fullmatch(command):
            # this is either a register read or set
            reg_letter, new_val = match.group("reg_letter"), match.group("new_val")
            if new_val is None:
                print(f"READ -> R{reg_letter} : {cpu.registers.get(ord('A') - ord(reg_letter)).unsigned_value:04x}")
            else:
                cpu.registers.set(ord("A") - ord(reg_letter), Int16(number_string_to_int(new_val)))
                print(f"WRITE -> R{reg_letter} : {cpu.registers.get(ord('A') - ord(reg_letter)).unsigned_value:04x}")
        elif match := DEBUG_MEMORY_EXPR.fullmatch(command):
            # this is either a memory read or set
            mem_addr, new_val = number_string_to_int(match.group("mem_addr")), match.group("new_val")
            if new_val is None:
                print(f"READ -> mem[{mem_addr:04x}] : {cpu.memory.get(mem_addr).unsigned_value:04x}")
            else:
                cpu.memory.set(mem_addr, Int16(number_string_to_int(new_val)))
                print(f"WRITE -> mem[{mem_addr:04x}] : {cpu.memory.get(mem_addr).unsigned_value:04x}")
        elif match := DEBUG_DISASSEMBLE_EXPR.fullmatch(command):
            literal, reg_letter, mem_addr = match.group("literal"), match.group("reg_letter"), match.group("mem_addr")

            instruction: base.Instruction | None = None
            instruction_args: tuple[int, ...] | None = None

            if any(i is not None for i in [literal, reg_letter, mem_addr]):
                prev_value = cpu.ir.value

                if literal is not None:
                    # parse to an integer and move the value into IR
                    cpu.ir.set(number_string_to_int(literal))
                elif reg_letter is not None:
                    # read integer from register and move into IR
                    cpu.ir.set(cpu.registers.get(ord("A") - ord(reg_letter)).unsigned_value)
                else:
                    # read integer from memory and move into IR
                    cpu.ir.set(cpu.memory.get(number_string_to_int(mem_addr)).unsigned_value)

                instruction, instruction_args = cpu.decode()

                cpu.ir.set(prev_value)

            if instruction is None or instruction_args is None:
                print("!! 'dis' failed - command syntax invalid")
            else:
                print(f"DISASSEMBLED -> {instruction.repr(instruction_args)}")

        # execution commands
        elif match := EXECUTION_STEP_EXPR.fullmatch(command):
            arg = match.group("arg")

            if arg is None:
                # do a single step
                arg = "1"

            step_instructions_run = 0

            condition: t.Callable[[], bool] | None = None
            if arg == ".":
                # step until breakpoint, halt (if enabled), or max number of instructions have been executed
                condition = lambda: True  # noqa: E731
            elif arg.isdigit():
                instructions_to_execute = int(arg)
                condition = lambda: step_instructions_run < instructions_to_execute  # noqa: E731
            else:
                print("!! 'step' failed - command syntax invalid")

            # will not run if we reached
            auto_halt_occurred = False
            while condition is not None and total_instructions_run < args.n_steps and condition():
                step_instructions_run += 1
                total_instructions_run += 1

                halted = cpu.step(detect_halt_loop=args.auto_halt)
                if halted:
                    print("AUTOHALT -> halt loop detected\n")
                    auto_halt_occurred = True
                    break

                # check if a breakpoint is satisfied
                # we check this AFTER running at least one instruction so that we won't get an infinite
                # loop of the same breakpoint over and over again
                should_break = False
                for bp_id, bp in enumerate(all_breakpoints):
                    if bp is None:
                        continue

                    # check if it is a line-number based breakpoint
                    if isinstance(bp, int):
                        if cpu.pc.value == bp:
                            print(f"BREAKPOINT -> hit breakpoint ID {bp_id}")
                            should_break = True
                            break
                        continue

                    # has to be a conditional breakpoint
                    if bp(cpu):
                        print(f"BREAKPOINT -> hit conditional breakpoint ID {bp_id}")
                        should_break = True
                        break

                if should_break:
                    break
            # we reached the max number of instructions - no longer need user input
            # set the command to 'quit' so that interactive mode will exit
            if total_instructions_run >= args.n_steps:
                print("<- max number of instructions reached ->")
                command = "quit"
                continue

            if auto_halt_occurred:
                command = "quit"
                continue
        elif match := EXECUTION_BREAKPOINT_EXPR.fullmatch(command):
            cmd, arg = match.group("cmd"), match.group("arg")

            if cmd == "set" and arg is not None:
                if arg.isdigit():
                    # line-based breakpoint
                    all_breakpoints.append(int(arg))
                    print(f"New breakpoint ID {len(all_breakpoints) - 1}")
                else:
                    # conditional breakpoint - TODO - figure out expression syntax
                    ...
            elif cmd == "list":
                filtered_breakpoints = [(i, bp) for i, bp in enumerate(all_breakpoints) if bp is not None]

                if not filtered_breakpoints:
                    print("No breakpoints set")
                else:
                    output_lines = [
                        "| ID | BREAKPOINT |",
                        "===================",
                    ]
                    for bp_id, bp in filtered_breakpoints:
                        bp_repr = bp
                        if isinstance(bp, int):
                            bp_repr = f"LINE {bp}"

                        output_lines.append(str(bp_id).rjust(4) + f" | {bp_repr}")
                    print("\n".join(output_lines))
            elif cmd == "del" and arg is not None and arg.isdigit():
                idx = int(arg)
                if idx >= len(all_breakpoints) or all_breakpoints[idx] is None:
                    print(f"Breakpoint with ID {idx} not found")
                else:
                    all_breakpoints[idx] = None
                    print(f"Removed breakpoint with ID {idx}")
            else:
                print("!! 'break' failed - command syntax invalid")

        # unrecognised command!
        else:
            print("!! unknown command")

        command = input(">>> ")


def run_cli(args: CliArgs) -> None:
    raw_instructions = parser.parse_dat_file(args.file)
    cpu = simulator.CPU(list(raw_instructions))

    elapsed_time: float
    if not args.interactive:
        # there will be no breakpoints, just run the requested number of instructions
        # and output final processor state
        before = time.perf_counter_ns()

        n = 0
        for n in range(args.n_steps):
            halted = cpu.step(detect_halt_loop=args.auto_halt)
            if halted:
                print("AUTOHALT -> halt loop detected\n")
                break

        elapsed_time = time.perf_counter_ns() - before
        instructions_run = n + 1
    else:
        before = time.perf_counter_ns()
        instructions_run = run_interactive_cli(cpu, args)
        elapsed_time = time.perf_counter_ns() - before

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
    register_state_lines[2] += "  NEGATIVE : " + ("ON" if cpu.alu.negative else "OFF")
    register_state_lines[3] += "  POSITIVE : " + ("ON" if cpu.alu.positive else "OFF")
    register_state_lines[4] += "  OVERFLOW : " + ("ON" if cpu.alu.overflow else "OFF")
    register_state_lines[5] += "  CARRY    : " + ("ON" if cpu.alu.carry else "OFF")
    register_state_lines[6] += "  ZERO     : " + ("ON" if cpu.alu.zero else "OFF")

    cpu.fetch()
    final_instruction, final_instruction_args = cpu.decode()

    output = [
        f"Instructions run     : {instructions_run}",
        f"Execution time       : {final_elapsed}",
        "",
        f"Program Counter      : {cpu.pc.value}",
        f"Instruction Register : {final_instruction.repr(final_instruction_args)}",
        "",
        *register_state_lines,
        "",
        "|     MEMORY STATE      |",
        "=========================",
        "LINE | HEX  | INSTRUCTION",
        "=========================",
        dis.decode_memory(cpu, include_pc=True),
    ]

    print("\n".join(output))
