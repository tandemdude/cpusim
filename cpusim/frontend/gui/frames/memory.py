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
from tkinter import messagebox
from tkinter import ttk

from cpusim.common.types import Int8
from cpusim.common.types import Int16
from cpusim.frontend.gui import base
from cpusim.frontend.gui.components import treeview


class MemoryFrame(base.AppFrame[base.CpuT]):
    def __init__(self, master: tk.Frame | tk.Tk, state: base.AppState[base.CpuT]) -> None:
        super().__init__(master, state, text="Memory")

        self._util_cpu: base.CpuT = state.cpu.__class__()

        cols = ("Addr", "8-bit", "16-bit", "Hex", "Instr")
        self._tree = treeview.EditableTreeView("Hex", 3, self.on_cell_edit, self, columns=cols, show="headings")
        # stop the user from being able to select a row, forces the selected row to match the PC value
        self._tree.bind("<Button-1>", lambda _: "break")

        for col in cols:
            self._tree.heading(col, text=col)
            self._tree.column(col, width=15)

        self._scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self._tree.yview)  # type: ignore
        self._tree.configure(yscrollcommand=self._scrollbar.set)
        self._scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._tree.pack(fill=tk.BOTH, expand=True)

        # monkeypatch out the write method so we can highlight rows that have been written to
        self._old_memory_set = self.state.cpu.memory.set
        self.state.cpu.memory.set = self._monkeypatched_memory_set

        self._written_rows: list[int] = []

        self.refresh()

    def _monkeypatched_memory_set(self, address: int, value: Int16) -> None:
        self._written_rows.append(address)
        self._old_memory_set(address, value)

    def on_cell_edit(self, iid: str, new_val: str) -> None:
        # check if valid hex
        try:
            new_int_val = int(new_val.lower().strip("0x"), 16)
        except ValueError:
            messagebox.showerror("Invalid hex value", f"{new_val!r} is not a valid hex number")  # pyright: ignore[reportUnknownMemberType]
            return

        memory_addr = int(iid.strip("mem_0x"), 16)
        self.state.cpu.memory.set(memory_addr, Int16(new_int_val))
        self.refresh()

    def refresh(self) -> None:
        for iid in self._tree.get_children():
            self._tree.delete(iid)

        for i in range(self.state.cpu.memory.size):
            value = self.state.cpu.memory.get(i)

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

        self._tree.item("mem_" + hex(self.state.cpu.pc.value), tags="pc")

        for addr in self._written_rows:
            self._tree.item("mem_" + hex(addr), tags="write")
        self._written_rows = []
