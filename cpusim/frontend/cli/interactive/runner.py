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
import dataclasses
import shlex
import traceback
import typing as t
from argparse import ArgumentError

from cpusim.backend import components
from cpusim.backend import simulators
from cpusim.backend.peripherals import gpio
from cpusim.common.types import Int8
from cpusim.common.types import Int16
from cpusim.frontend.cli.interactive import converters
from cpusim.frontend.cli.interactive import parser

CpuT = t.TypeVar("CpuT", simulators.CPU1a, simulators.CPU1d)


@dataclasses.dataclass(slots=True)
class LineBreakpoint:
    value: int
    enabled: bool


@dataclasses.dataclass(slots=True)
class ConditionalBreakpoint:
    value: str
    enabled: bool


class InteractiveDebugger(abc.ABC, t.Generic[CpuT]):
    __slots__ = ("_conditional_breakpoints", "_cpu", "_lineno_breakpoints", "_next_breakpoint_id", "halted")

    def __init__(self, cpu: CpuT) -> None:
        self._cpu = cpu

        self._next_breakpoint_id = 0
        self._lineno_breakpoints: dict[int, LineBreakpoint] = {}
        self._conditional_breakpoints: dict[int, ConditionalBreakpoint] = {}

        self.halted = False

    def _check_breakpoints(self) -> tuple[bool, int]:
        for id, bp in self._lineno_breakpoints.items():
            if not bp.enabled:
                continue

            if self._cpu.pc.value == bp.value:
                return True, id

        context = self._conditional_breakpoint_context()
        for id, bp in self._conditional_breakpoints.items():
            if not bp.enabled:
                continue

            if eval(bp.value, context):
                return True, id

        return False, -1

    def _justify_row(self, row: t.Sequence[str], sizes: t.Sequence[int]) -> str:
        return " | ".join(cell.ljust(sizes[i]) for i, cell in enumerate(row))

    def _justify_rows(self, rows: t.Sequence[t.Sequence[str]]) -> str:
        col_widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
        justified_rows: list[str] = []
        for row in rows:
            justified_rows.append(self._justify_row(row, col_widths))

        return "\n".join(justified_rows)

    def _info_registers(self, registers: dict[str, int]) -> str:
        rows: list[tuple[str, str, str, str]] = [("Name", "8-bit", "16-bit", "Hex")]
        for register in registers.items():
            rows.append(
                (
                    register[0],
                    str(Int8(register[1]).signed_value),
                    str(Int16(register[1]).signed_value),
                    hex(register[1]),
                )
            )

        return self._justify_rows(rows)

    @abc.abstractmethod
    def _conditional_breakpoint_context(self) -> dict[str, t.Any]: ...

    @abc.abstractmethod
    def info_registers(self) -> str: ...

    def info_memory(self) -> str:
        # addr, 8-bit dec, 16-bit dec, hex, decoded, is_zero
        old_val = self._cpu.ir.value

        rows: list[tuple[str, str, str, str, str, bool]] = [("Addr", "8-bit", "16-bit", "Hex", "Disassembled", False)]
        for addr in range(self._cpu.memory.size):
            if addr in self._cpu.memory._memmap_addr:
                rows.append((hex(addr), "?", "?", "?", f"mem-mapped ({self._cpu.memory._memmap_addr[addr]})", False))
                continue

            value = self._cpu.memory.get(addr)

            self._cpu.ir.set(value.unsigned_value)
            try:
                instruction, args = self._cpu.decode()
                instruction_repr = instruction.repr(args)
            except NotImplementedError:
                instruction_repr = "????"

            rows.append(
                (
                    hex(addr),
                    str(Int8(value.unsigned_value).signed_value),
                    str(value.signed_value),
                    hex(value.unsigned_value),
                    instruction_repr,
                    value.unsigned_value == 0,
                )
            )

        col_widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0][:-1]))]  # type: ignore[reportArgumentType]
        justified_rows: list[str] = []

        zero_addrs: list[str] = []
        known_zero_row = next(filter(lambda row: row[-1], rows))
        for row in rows:
            if row[-1]:
                zero_addrs.append(row[0])
                continue

            if len(zero_addrs) > 3:
                justified_rows.append(f"<-- ... {len(zero_addrs)} zeros -->")
                zero_addrs = []
            else:
                for addr in zero_addrs:
                    justified_rows.append(self._justify_row([addr, *known_zero_row[1:-1]], col_widths))

            justified_rows.append(self._justify_row(row[:-1], col_widths))

        if zero_addrs:
            justified_rows.append(f"<-- ... {len(zero_addrs)} zeros -->")

        self._cpu.ir.set(old_val)
        return "\n".join(justified_rows)

    def info_breakpoints(self) -> str:
        rows: list[tuple[str, str, str, str]] = [("ID", "Type", "Enabled", "Value")]
        for id, bp in sorted([*self._lineno_breakpoints.items(), *self._conditional_breakpoints.items()]):
            rows.append((str(id), "LINE" if isinstance(bp, LineBreakpoint) else "COND", str(bp.enabled), str(bp.value)))

        return self._justify_rows(rows)

    def info_flags(self) -> str:
        rows: list[tuple[str, str]] = [("Name", "Value")]

        flag_attrs = ["negative", "positive", "overflow", "carry", "zero"]
        for attr in flag_attrs:
            rows.append((attr, str(getattr(self._cpu.alu, attr))))

        return self._justify_rows(rows)

    def info_bugtrap(self) -> str:
        if self._cpu.gpio is None:
            return "Bug trap hardware not installed."

        bugtrap = next((d for d in self._cpu.gpio._devices if isinstance(d, gpio.BugTrap)), None)
        if bugtrap is None:
            return "Bug trap hardware not installed."

        rows: list[tuple[str, str]] = [
            ("Name", "Value"),
            ("Trap", "CLOSED" if bugtrap.trap_closed else "OPEN"),
            ("LED", "ON" if bugtrap.led_on else "OFF"),
            ("Mode", "MANUAL" if bugtrap.mode_switch_manual else "AUTO"),
            ("Fire", "ON" if bugtrap.fire_button_pressed else "OFF"),
            ("Sensor 1", "ON" if bugtrap.sensor_1_triggered else "OFF"),
            ("Sensor 2", "ON" if bugtrap.sensor_2_triggered else "OFF"),
        ]
        return self._justify_rows(rows)

    def step(self, n: int) -> str:
        out: list[str] = []
        for _ in range(n):
            self.halted = self._cpu.step()
            if self.halted:
                out.append(f"Halt-loop reached at address {hex(self._cpu.pc.value)}. Exiting...")
                break

            instruction, args = self._cpu.decode()
            out.append(instruction.repr(args))

            should_break, bp_id = self._check_breakpoints()
            if should_break:
                out.append(f"Triggered breakpoint ID {bp_id}. Pausing...")
                break

        return "\n".join(out)

    def continue_(self) -> str:
        out: list[str] = []

        step_count = 0
        while True:
            self.halted = self._cpu.step()
            step_count += 1
            if self.halted:
                out.append(
                    f"Executed {step_count} instructions\nHalt-loop reached "
                    f"at address {hex(self._cpu.pc.value)}. Exiting..."
                )
                break

            should_break, bp_id = self._check_breakpoints()
            if should_break:
                out.append(f"Executed {step_count} instructions\nTriggered breakpoint ID {bp_id}. Pausing...")
                break

        return "\n".join(out)

    def _value_for_target(self, target: converters.Address | converters.Register) -> Int16:
        if isinstance(target, converters.Address):
            return self._cpu.memory.get(target.value)

        register = getattr(self._cpu, target.attr_name)
        if isinstance(register, components.IntRegister):
            return Int16(register.value)

        return t.cast("components.Registers", register).get(target.id)

    def breakpoint(
        self,
        subcommand: t.Literal["create", "delete", "enable", "disable"],
        expr: list[str] | None = None,
        line: int | None = None,
        bp_id: int | None = None,
        error_if_invalid: bool = False,
    ) -> str:
        if bp_id is not None and bp_id not in self._lineno_breakpoints and bp_id not in self._conditional_breakpoints:
            return f"No breakpoint with ID {bp_id} exists."

        if subcommand == "create":
            if expr is not None:
                bp_expr = "".join(expr)

                try:
                    eval(bp_expr, self._conditional_breakpoint_context())
                except Exception as e:
                    if error_if_invalid:
                        raise e
                    return f"Expression validation failed:\n{traceback.format_exception(e, limit=0)}"

                self._conditional_breakpoints[self._next_breakpoint_id] = ConditionalBreakpoint(bp_expr, True)
            elif line is not None:
                self._lineno_breakpoints[self._next_breakpoint_id] = LineBreakpoint(line, True)

            self._next_breakpoint_id += 1
            return (
                f"Created new {'conditional' if expr is not None else 'line'} "
                f"breakpoint with ID {self._next_breakpoint_id - 1}"
            )

        assert bp_id is not None
        if subcommand == "delete":
            self._lineno_breakpoints.pop(bp_id)
            self._conditional_breakpoints.pop(bp_id)
            return f"Deleted breakpoint with ID {bp_id}"

        # otherwise subcommand must be "enable" or "disable"
        new_val = subcommand == "enable"
        if bp_id in self._lineno_breakpoints:
            self._lineno_breakpoints[bp_id].enabled = True
        elif bp_id in self._conditional_breakpoints:
            self._conditional_breakpoints[bp_id].enabled = True
        return f"{'Enabled' if new_val else 'Disabled'} breakpoint with ID {bp_id}"

    def disassemble(self, target: converters.Address | converters.Register) -> str:
        out: list[str] = []

        to_disassemble = self._value_for_target(target).unsigned_value
        if isinstance(target, converters.Address):
            out.append(f"Instruction at address {hex(target.value)}:")
        else:
            out.append(f"Instruction in register {target.register_name}:")

        old_ir_value = self._cpu.ir.value
        self._cpu.ir.set(to_disassemble)

        instruction, args = self._cpu.decode()
        self._cpu.ir.set(old_ir_value)
        out.append("    " + instruction.repr(args))

        return "\n".join(out)

    def print(self, target: converters.Address | converters.Register) -> str:
        out: list[str] = []

        value = self._value_for_target(target)

        if isinstance(target, converters.Address):
            out.append(f"Value at address {hex(target.value)}:")
        else:
            out.append(f"Value in register {target.register_name}:")

        out.append(
            f"    Hex: {hex(value.unsigned_value)}\n"
            f"    Bin: {bin(value.unsigned_value)}\n"
            f"    Dec: {value.unsigned_value} (unsigned)\n"
            f"         {Int8(value.unsigned_value).signed_value} (8bit signed)\n"
            f"         {value.signed_value} (16bit signed)"
        )
        return "\n".join(out)

    def set(self, target: converters.Address | converters.Register, value: int) -> str:
        if isinstance(target, converters.Address):
            self._cpu.memory.set(target.value, Int16(value))
            return f"Set value at address {hex(target.value)} to {hex(value)}"

        if target.attr_name == "registers":
            getattr(self._cpu, target.attr_name).set(target.id, Int16(value))
        else:
            getattr(self._cpu, target.attr_name).set(value)

        return f"Set register {target.register_name} to {hex(value)}"

    def execute_command(self, raw_command: str) -> str | None:
        try:
            arguments = parser.parse_args(shlex.split(raw_command.lower()))
        except ArgumentError as e:
            return f"Error: {e.message}\nRun '<command> -h' for usage details"

        if arguments.help:
            return None

        if arguments.command == "quit":
            self.halted = True
            return "Quit command received. Exiting..."

        assert arguments.command is not None
        match arguments.command:
            case "info":
                assert arguments.item is not None
                if arguments.item == "registers":
                    return self.info_registers()
                elif arguments.item == "breakpoints":
                    return self.info_breakpoints()
                elif arguments.item == "memory":
                    return self.info_memory()
                elif arguments.item == "bugtrap":
                    return self.info_bugtrap()
                return self.info_flags()
            case "step":
                assert arguments.number is not None
                return self.step(arguments.number)
            case "continue":
                return self.continue_()
            case "breakpoint":
                assert arguments.breakpoint_subcommand is not None
                return self.breakpoint(
                    arguments.breakpoint_subcommand,
                    getattr(arguments, "breakpoint_create_expr", None),
                    getattr(arguments, "breakpoint_create_line", None),
                    getattr(arguments, "id", None),
                )
            case "disassemble":
                assert arguments.target is not None
                return self.disassemble(arguments.target)
            case "print":
                assert arguments.target is not None
                return self.print(arguments.target)
            case "set":
                assert arguments.target is not None
                assert arguments.value is not None
                return self.set(arguments.target, arguments.value)

        return None


class CPU1aInteractiveDebugger(InteractiveDebugger[simulators.CPU1a]):
    __slots__ = ()

    def info_registers(self) -> str:
        return super()._info_registers({"pc": self._cpu.pc.value, "ir": self._cpu.ir.value, "acc": self._cpu.acc.value})

    def _conditional_breakpoint_context(self) -> dict[str, t.Any]:
        return {
            "pc": self._cpu.pc.value,
            "ir": self._cpu.ir.value,
            "acc": Int8(self._cpu.acc.value),
            "mem": self._cpu.memory,
            "alu": self._cpu.alu,
        }


class CPU1dInteractiveDebugger(InteractiveDebugger[simulators.CPU1d]):
    __slots__ = ()

    def info_registers(self) -> str:
        registers: dict[str, t.Any] = {"pc": self._cpu.pc.value, "ir": self._cpu.ir.value}
        for i in range(self._cpu.registers._register_limit):
            registers[f"r{chr(ord('a') + i)}"] = self._cpu.registers.get(i).unsigned_value

        return self._info_registers(registers)

    def _conditional_breakpoint_context(self) -> dict[str, t.Any]:
        out: dict[str, t.Any] = {"pc": self._cpu.pc.value, "ir": self._cpu.ir.value, "mem": self._cpu.memory}
        for i in range(self._cpu.registers._register_limit):
            out[f"r{chr(ord('a') + i)}"] = self._cpu.registers.get(i)

        return out
