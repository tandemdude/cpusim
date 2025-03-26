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
from tkinter import ttk

from cpusim.backend import simulators
from cpusim.common.types import Int8
from cpusim.common.types import Int16
from cpusim.frontend.gui.components import treeview

CpuT = t.TypeVar("CpuT", simulators.CPU1a, simulators.CPU1d)


class MemoryFrame(tk.LabelFrame, t.Generic[CpuT]):
    def __init__(self, root: tk.Frame, cpu: CpuT) -> None:
        super().__init__(root, text="Memory")

        self._util_cpu: CpuT = cpu.__class__()

        self.pc = cpu.pc
        self.mem = cpu.memory

        cols = ("Addr", "8-bit", "16-bit", "Hex", "Instr")
        self._tree = treeview.EditableTreeView("Hex", 3, self.on_cell_edit, self, columns=cols, show="headings")
        # stop the user from being able to select a row, forces the selected row to match the PC value
        self._tree.bind("<Button-1>", lambda _: "break")

        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=15)

        self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=self._scrollbar.set)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._tree.pack(fill=tk.BOTH, expand=True)

        self.refresh()

    def on_cell_edit(self, iid: str, new_val: str) -> None:
        # check if valid hex
        try:
            new_int_val = int(new_val.lower().strip("0x"), 16)
        except ValueError:
            messagebox.showerror("Invalid hex value", f"{new_val!r} is not a valid hex number")
            return

        memory_addr = int(iid.strip("mem_0x"), 16)
        self.mem.set(memory_addr, Int16(new_int_val))
        # TODO - we can get away with refreshing only the single row here instead
        self.refresh()

    def refresh(self) -> None:
        for iid in self._tree.get_children():
            self._tree.delete(iid)

        for i in range(self.mem.size):
            value = self.mem.get(i)

            self._util_cpu.ir.set(value.unsigned_value)

            try:
                instr, args = self._util_cpu.decode()
                instruction_repr = instr.repr(args)
            except NotImplementedError:
                instruction_repr = "????"

            self._tree.insert(
                "",
                "end",
                iid="mem_" + hex(i),
                values=(
                    hex(i),
                    str(Int8(value.unsigned_value).signed_value),
                    str(value.signed_value),
                    f"0x{value.unsigned_value:04x}",
                    instruction_repr,
                ),
            )

        self._tree.selection_set("mem_" + hex(self.pc.value))
