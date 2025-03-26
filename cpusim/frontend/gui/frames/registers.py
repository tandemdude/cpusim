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
from tkinter import messagebox

from cpusim.backend import simulators
from cpusim.common.types import Int8
from cpusim.common.types import Int16
from cpusim.frontend.gui.components import treeview

CpuT = t.TypeVar("CpuT", simulators.CPU1a, simulators.CPU1d)


class RegistersFrame(tk.LabelFrame, t.Generic[CpuT]):
    def __init__(self, root: tk.Frame, cpu: CpuT) -> None:
        super().__init__(root, text="Registers")

        self.cpu = cpu

        cols = ("Name", "8-bit", "16-bit", "Hex")
        self._tree = treeview.EditableTreeView(
            "Hex", 3, self.on_cell_edit, self, exclude_iids=("divider",), columns=cols, show="headings"
        )

        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=15)

        self._tree.pack(fill=tk.BOTH, expand=True)

        self.refresh()

    def on_cell_edit(self, iid: str, new_val: str) -> None:
        try:
            parsed_val = int(new_val.lower().strip("0x"), 16)
        except ValueError:
            messagebox.showerror("Invalid hex value", f"{new_val!r} is not a valid hex number")
            return

        if iid == "pc":
            self.cpu.pc.set(Int16(parsed_val))
        elif iid == "ir":
            self.cpu.ir.set(Int16(parsed_val))
        elif iid == "acc":
            self.cpu.acc.set(Int8(parsed_val).unsigned_value)
        else:
            # set general purpose registers
            self.cpu.registers.set(ord(iid[1]) - ord("a"), Int16(parsed_val))

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

        _insert("pc", self.cpu.pc.value)
        _insert("ir", self.cpu.ir.value)

        # divider line
        self._tree.insert("", "end", iid="divider", values=("--", "--", "--", "--"))

        if isinstance(self.cpu, simulators.CPU1a):
            _insert("acc", self.cpu.acc.value)
        else:
            for i in range(self.cpu.registers._register_limit):
                _insert(f"r{chr(ord('a') + i)}", self.cpu.registers.get(i).unsigned_value)
