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
import tkinter as tk
import typing as t

from cpusim.frontend.cli.interactive import runner
from cpusim.frontend.gui import base
from cpusim.frontend.gui.frames import breakpoints
from cpusim.frontend.gui.frames import flags
from cpusim.frontend.gui.frames import memory
from cpusim.frontend.gui.frames import registers
from cpusim.frontend.gui.frames import toolbar
from cpusim.frontend.gui.frames.peripherals import bug_trap


class GuiApp(tk.Tk, t.Generic[base.CpuT]):
    def __init__(
        self,
        mem: list[int],
        cpu: type[base.CpuT],
        cpu_configurer: t.Callable[[base.CpuT], base.CpuT],
        debugger: type[runner.InteractiveDebugger[base.CpuT]],
        *args: t.Any,
        **kwargs: t.Any,
    ) -> None:
        super().__init__(*args, **kwargs)

        self._cpu_configurer = cpu_configurer

        self.title("CPUSim GUI v0")
        self.geometry("1200x800")

        self.mem: list[int]
        self.state: base.AppState[base.CpuT]

        self._toolbar_frame: base.AppFrame[base.CpuT]

        self._mem_register_frame: tk.Frame
        self._memory_frame: base.AppFrame[base.CpuT]
        self._registers_frame: base.AppFrame[base.CpuT]

        self._bp_flag_frame: tk.Frame
        self._breakpoints_frame: base.AppFrame[base.CpuT]
        self._flags_frame: base.AppFrame[base.CpuT]

        self._bug_trap_window: bug_trap.BugTrapSimulatorWindow[base.CpuT] | None

        self.init(mem, cpu, debugger)

    def init(self, mem: list[int], cpu: type[base.CpuT], debugger: type[runner.InteractiveDebugger[base.CpuT]]) -> None:
        self.mem = mem
        self.state = base.AppState((c := self._cpu_configurer(cpu(mem))), debugger(c), False)

        self._toolbar_frame = toolbar.ToolbarFrame(self, self.state, self.reset, self.refresh)
        self._toolbar_frame.pack(fill=tk.X, padx=5, pady=5)

        self._mem_register_frame = tk.Frame(self)
        self._mem_register_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._memory_frame = memory.MemoryFrame(self._mem_register_frame, self.state)
        self._memory_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._registers_frame = registers.RegistersFrame(self._mem_register_frame, self.state)
        self._registers_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._bp_flag_frame = tk.Frame(self)
        self._bp_flag_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._breakpoints_frame = breakpoints.BreakpointsFrame(self._bp_flag_frame, self.state)
        self._breakpoints_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._flags_frame = flags.FlagsFrame(self._bp_flag_frame, self.state)
        self._flags_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self._bug_trap_window = (
            bug_trap.BugTrapSimulatorWindow(self, self.state) if self.state.cpu.gpio is not None else None
        )

    def reset(self) -> None:
        self._toolbar_frame.destroy()
        self._mem_register_frame.destroy()
        self._bp_flag_frame.destroy()

        if self._bug_trap_window is not None:
            self._bug_trap_window.destroy()

        self.init(self.mem, self.state.cpu.__class__, self.state.debugger.__class__)  # type: ignore[reportArgumentType]
        self.refresh()

    def refresh(self) -> None:
        self._memory_frame.refresh()
        self._registers_frame.refresh()
        self._breakpoints_frame.refresh()
        self._flags_frame.refresh()

        if self._bug_trap_window is not None:
            self._bug_trap_window.refresh()

    def run(self) -> None:
        self.mainloop()
