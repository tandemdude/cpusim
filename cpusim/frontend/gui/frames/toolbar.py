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

import tkinter as tk
import typing as t

from cpusim.frontend.gui import base


class ToolbarFrame(base.AppFrame[base.CpuT]):
    def __init__(
        self,
        master: tk.Frame | tk.Tk,
        state: base.AppState[base.CpuT],
        reset_parent_fn: t.Callable[[], None],
        refresh_parent_fn: t.Callable[[], None],
        **kwargs: t.Any,
    ) -> None:
        super().__init__(master, state, text="Tools", **kwargs)

        self.refresh_parent_fn = refresh_parent_fn

        self.state.state_var.set("RUN")
        self.state.breakpoint_var.set("---")

        self._reset_btn = tk.Button(self, text="Reset", command=reset_parent_fn)
        self._reset_btn.grid(row=0, column=0, padx=5, pady=5)

        self._step_btn = tk.Button(self, text="Step Over", command=self._on_step)
        self._step_btn.grid(row=0, column=1, padx=5, pady=5)

        self._continue_btn = tk.Button(self, text="Continue", command=self._on_continue)
        self._continue_btn.grid(row=0, column=2, padx=5, pady=5)

        self._state_frame = tk.LabelFrame(self, text="State")
        self._state_frame.grid(row=0, column=3, padx=10, pady=5, sticky="e")
        self._state_label = tk.Label(self._state_frame, textvariable=self.state.state_var, background="lawn green")
        self._state_label.pack(padx=5, pady=5)

        self._triggered_breakpoint_frame = tk.LabelFrame(self, text="Breakpoint Hit")
        self._triggered_breakpoint_frame.grid(row=0, column=4, padx=10, pady=5, sticky="e")
        self._triggered_breakpoint_label = tk.Label(
            self._triggered_breakpoint_frame, textvariable=self.state.breakpoint_var
        )
        self._triggered_breakpoint_label.pack(padx=5, pady=5)

        self.columnconfigure(3, weight=1)

    def _halt(self) -> None:
        self.state.state_var.set("HLT")
        self._step_btn.config(state=tk.DISABLED)
        self._continue_btn.config(state=tk.DISABLED)

        self._state_label.configure(background="orange red")

    def _on_step(self) -> None:
        self.state.breakpoint_var.set("---")
        self.state.state_var.set("RUN")
        self._state_label.configure(background="lawn green")

        halted = self.state.cpu.step()

        if halted:
            self._halt()

        self.refresh_parent_fn()

    def _on_continue(self) -> None:
        self.state.breakpoint_var.set("---")

        while True:
            halted = self.state.cpu.step()

            if halted:
                self._halt()
                break

            broken, bp_id = self.state.debugger._check_breakpoints()
            if broken:
                self.state.state_var.set("BRK")
                self.state.breakpoint_var.set(str(bp_id))
                self._state_label.configure(background="yellow")
                break

        self.refresh_parent_fn()
