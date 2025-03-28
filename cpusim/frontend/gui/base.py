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
import tkinter as tk
import typing as t

from cpusim.backend import simulators
from cpusim.frontend.cli.interactive import runner

CpuT = t.TypeVar("CpuT", simulators.CPU1a, simulators.CPU1d)


@dataclasses.dataclass(slots=True)
class AppState(t.Generic[CpuT]):
    cpu: CpuT
    debugger: runner.InteractiveDebugger[CpuT]
    halted: bool

    state_var: tk.StringVar = dataclasses.field(init=False, default_factory=tk.StringVar)
    breakpoint_var: tk.StringVar = dataclasses.field(init=False, default_factory=tk.StringVar)


class AppFrame(tk.LabelFrame, t.Generic[CpuT], abc.ABC):
    def __init__(self, master: tk.Frame | tk.Tk, state: AppState[CpuT], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.state = state

    @abc.abstractmethod
    def refresh(self) -> None: ...
