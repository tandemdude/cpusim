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

__all__ = ["run_gui"]

import functools
import typing as t

from cpusim.backend import simulators
from cpusim.backend.peripherals import gpio
from cpusim.frontend.cli.interactive import runner
from cpusim.frontend.gui import app
from cpusim.frontend.gui import base

if t.TYPE_CHECKING:
    from cpusim.__main__ import CliArguments


def _noop(cpu: base.CpuT) -> base.CpuT:
    return cpu


def _enable_bug_trap(cpu: base.CpuT, addr: int) -> base.CpuT:
    cpu.gpio = gpio.GPIO(cpu, gpio.GPIOConfig(2, addr))
    cpu.gpio.set_device(0, gpio.BugTrap())
    return cpu


def run_gui(args: CliArguments, mem: list[int]) -> None:
    cpu_configurer = _noop
    if args.enable_bug_trap:
        cpu_configurer = functools.partial(_enable_bug_trap, addr=args.bug_trap_address)

    if args.arch == "1a":
        app.GuiApp(mem, simulators.CPU1a, cpu_configurer, runner.CPU1aInteractiveDebugger).run()
        return

    app.GuiApp(mem, simulators.CPU1d, cpu_configurer, runner.CPU1dInteractiveDebugger).run()
