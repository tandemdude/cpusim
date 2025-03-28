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

import functools
import tkinter as tk
import typing as t
from tkinter import messagebox

from cpusim.backend import simulators
from cpusim.common.types import Int8
from cpusim.common.types import Int16
from cpusim.frontend.gui import base
from cpusim.frontend.gui.components import treeview


class RegistersFrame(base.AppFrame[base.CpuT]):
    def __init__(self, master: tk.Frame | tk.Tk, state: base.AppState[base.CpuT]) -> None:
        super().__init__(master, state, text="Registers")

        cols = ("Name", "8-bit", "16-bit", "Hex")
        self._tree = treeview.EditableTreeView(
            "Hex", 3, self.on_cell_edit, self, exclude_iids=("divider",), columns=cols, show="headings"
        )

        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=15)

        self._tree.pack(fill=tk.BOTH, expand=True)

        if isinstance(self.state.cpu, simulators.CPU1a):
            self.state.cpu.acc.set = functools.partial(
                self._monkeypatched_int_register_set, name="acc", orig=self.state.cpu.acc.set
            )
        else:
            self.state.cpu.registers.set = functools.partial(
                self._monkeypatched_gp_register_set, orig=self.state.cpu.registers.set
            )

        self._modified_registers: list[str] = []

        self.refresh()

    def _monkeypatched_int_register_set(self, val: int, name: str, orig: t.Callable[[int], None]) -> None:
        self._modified_registers.append(name)
        orig(val)

    def _monkeypatched_gp_register_set(self, idx: int, val: Int16, orig: t.Callable[[int, Int16], None]) -> None:
        self._modified_registers.append(f"r{chr(ord('a') + idx)}")
        orig(idx, val)

    def on_cell_edit(self, iid: str, new_val: str) -> None:
        try:
            parsed_val = int(new_val.lower().strip("0x"), 16)
        except ValueError:
            messagebox.showerror("Invalid hex value", f"{new_val!r} is not a valid hex number")
            return

        if iid == "pc":
            self.state.cpu.pc.set(Int16(parsed_val))
        elif iid == "ir":
            self.state.cpu.ir.set(Int16(parsed_val))
        elif iid == "acc":
            self.state.cpu.acc.set(Int8(parsed_val).unsigned_value)
        else:
            # set general purpose registers
            self.state.cpu.registers.set(ord(iid[1]) - ord("a"), Int16(parsed_val))

        self.refresh()

    def refresh(self) -> None:
        for iid in self._tree.get_children():
            self._tree.delete(iid)

        def _insert(name: str, val: int) -> None:
            self._tree.insert(
                "",
                "end",
                iid=name,
                values=(name, str(Int8(val).signed_value), str(Int16(val).signed_value), f"0x{val:04x}"),
            )

        _insert("pc", self.state.cpu.pc.value)
        _insert("ir", self.state.cpu.ir.value)

        # divider line
        self._tree.insert("", "end", iid="divider", values=("--", "--", "--", "--"))

        if isinstance(self.state.cpu, simulators.CPU1a):
            _insert("acc", self.state.cpu.acc.value)
        else:
            for i in range(self.state.cpu.registers._register_limit):
                _insert(f"r{chr(ord('a') + i)}", self.state.cpu.registers.get(i).unsigned_value)

        for reg in self._modified_registers:
            self._tree.item(reg, tags="write")
        self._modified_registers = []
