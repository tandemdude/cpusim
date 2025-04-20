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

import collections
import functools
import tkinter as tk
import traceback
from tkinter import messagebox
from tkinter import ttk

from cpusim.frontend.cli.interactive import converters
from cpusim.frontend.cli.interactive import runner
from cpusim.frontend.gui import base


class BreakpointsFrame(base.AppFrame[base.CpuT]):
    def __init__(self, master: tk.Frame | tk.Tk, state: base.AppState[base.CpuT]) -> None:
        super().__init__(master, state, text="Breakpoints")

        self._create_bp_frame = tk.LabelFrame(self, text="Create Breakpoint")
        self._create_bp_frame.pack(padx=5, pady=5)

        self._type_label = tk.Label(self._create_bp_frame, text="Type:")
        self._type_label.grid(row=0, column=0, padx=5, pady=5)

        self._type_var = tk.StringVar(value="LINE")
        self._type_dropdown = ttk.Combobox(
            self._create_bp_frame, textvariable=self._type_var, values=["LINE", "COND"], state="readonly"
        )
        self._type_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self._value_label = tk.Label(self._create_bp_frame, text="Value:")
        self._value_label.grid(row=0, column=2, padx=5, pady=5)

        self._value_entry = tk.Entry(self._create_bp_frame)
        self._value_entry.grid(row=0, column=3, padx=5, pady=5)

        self._create_btn = tk.Button(self._create_bp_frame, text="+", fg="green", command=self._create_breakpoint)
        self._create_btn.grid(row=0, column=4, padx=5, pady=5)

        self._breakpoints_table: tk.Frame | None = None
        self._vars: dict[int, tk.IntVar] = collections.defaultdict(tk.IntVar)

        self.refresh()

    def _create_breakpoint(self) -> None:
        raw = self._value_entry.get()
        if self._type_var.get() == "LINE":
            try:
                value = converters.number_string_to_int(raw)
            except ValueError:
                messagebox.showerror("Parsing Error", f"{raw} cannot be parsed to hex, binary, or decimal integer")  # type: ignore[reportUnknownMemberType]
                return
            self.state.debugger.breakpoint("create", line=value)
        else:
            try:
                self.state.debugger.breakpoint("create", expr=[raw], error_if_invalid=True)
            except Exception as e:
                messagebox.showerror("Expression Error", "\n".join(traceback.format_exception(e, limit=0)))  # type: ignore[reportUnknownMemberType]
                return

        self._value_entry.delete(0, "end")

        self.refresh()

    def _delete_breakpoint(self, id_: int) -> None:
        self.state.debugger._lineno_breakpoints.pop(id_, None)
        self.state.debugger._conditional_breakpoints.pop(id_, None)
        self._vars.pop(id_, None)

        self.refresh()

    def _on_toggle(self, id_: int) -> None:
        if (bp := self.state.debugger._lineno_breakpoints.get(id_)) is not None or (
            bp := self.state.debugger._conditional_breakpoints.get(id_)
        ) is not None:
            bp.enabled = not bp.enabled

    def _build_breakpoint_table_header(self) -> None:
        if self._breakpoints_table is not None:
            self._breakpoints_table.destroy()

        self._breakpoints_table = tk.Frame(self)
        self._breakpoints_table.pack(padx=5, pady=5)

        tk.Label(self._breakpoints_table, text="ID", relief=tk.RIDGE, width=12).grid(row=0, column=0)
        tk.Label(self._breakpoints_table, text="Type", relief=tk.RIDGE, width=12).grid(row=0, column=1)
        tk.Label(self._breakpoints_table, text="Value", relief=tk.RIDGE, width=12).grid(row=0, column=2)
        tk.Label(self._breakpoints_table, text="Enabled", relief=tk.RIDGE, width=12).grid(row=0, column=3)
        tk.Label(self._breakpoints_table, text="Delete", relief=tk.RIDGE, width=12).grid(row=0, column=4)

    def refresh(self) -> None:
        self._build_breakpoint_table_header()
        assert self._breakpoints_table is not None

        all_breakpoints = [
            *self.state.debugger._lineno_breakpoints.items(),
            *self.state.debugger._conditional_breakpoints.items(),
        ]
        for i, elem in enumerate(sorted(all_breakpoints, key=lambda e: e[0])):
            tk.Label(
                self._breakpoints_table,
                text=str(elem[0]),
                relief=tk.FLAT,
                width=12,
                background="yellow"
                if str(elem[0]) == self.state.breakpoint_var.get()
                else self._breakpoints_table.cget("background"),
            ).grid(row=i + 1, column=0)
            tk.Label(
                self._breakpoints_table,
                text="LINE" if isinstance(elem[1], runner.LineBreakpoint) else "COND",
                relief=tk.FLAT,
                width=12,
            ).grid(row=i + 1, column=1)
            tk.Label(self._breakpoints_table, text=str(elem[1].value), relief=tk.FLAT, width=12).grid(
                row=i + 1, column=2
            )

            self._vars[elem[0]].set(int(elem[1].enabled))

            tk.Checkbutton(
                self._breakpoints_table,
                variable=self._vars[elem[0]],
                onvalue=1,
                offvalue=0,
                command=functools.partial(self._on_toggle, id_=elem[0]),
            ).grid(row=i + 1, column=3)

            tk.Button(
                self._breakpoints_table,
                text="X",
                fg="red",
                command=functools.partial(self._delete_breakpoint, id_=elem[0]),
            ).grid(row=i + 1, column=4)
