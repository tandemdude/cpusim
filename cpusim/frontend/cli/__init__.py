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

__all__ = ["run_cli"]

import typing as t

from cpusim.backend import simulators
from cpusim.backend.peripherals import gpio
from cpusim.frontend.cli.interactive import runner

if t.TYPE_CHECKING:
    from cpusim.__main__ import CliArguments


def run_cli(args: CliArguments, mem: list[int]) -> None:
    cpu = simulators.CPU1a(mem) if args.arch == "1a" else simulators.CPU1d(mem)

    if args.bug_trap is not None:
        cpu.gpio = gpio.GPIO(cpu, gpio.GPIOConfig(2, args.bug_trap[0]))
        cpu.gpio.set_device(0, gpio.BugTrap())

    debugger = runner.CPU1aInteractiveDebugger(cpu) if args.arch == "1a" else runner.CPU1dInteractiveDebugger(cpu)  # type: ignore[reportArgumentType]
    if not args.interactive:
        # run requested number of steps
        instructions_run, halted = 0, False
        assert args.steps is not None
        for _ in range(args.steps):
            instructions_run += 1
            halted = cpu.step()

            if halted:
                break

        if halted:
            print(
                f"Executed {instructions_run} instructions\n"
                f"Halt-loop reached at address {hex(cpu.pc.value)}. Exiting..."
            )
        else:
            print(f"Executed {instructions_run} instructions")
    else:
        # do interactive mode i/o
        print("Welcome to the interactive debugger!\n    '-h' or '--help' to show commands\n    'quit' to quit")
        while not debugger.halted:
            command = input("(idb) ")

            out = debugger.execute_command(command)
            if out is not None:
                print(out)

    # dump processor state
    print("\n== Final processor state ==")
    print("\nMemory:")
    print(debugger.info_memory())
    print("\nRegisters:")
    print(debugger.info_registers())
    print("\nFlags:")
    print(debugger.info_flags())
