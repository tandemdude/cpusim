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

if t.TYPE_CHECKING:
    from cpusim.backend.components import alu as alu_


class FlagsFrame(tk.LabelFrame):
    def __init__(self, root: tk.Frame, alu: alu_.ALU[t.Any]) -> None:
        super().__init__(root, text="ALU Flags")

        self.alu = alu
        self.vars: dict[str, tk.IntVar] = {
            "negative": tk.IntVar(),
            "positive": tk.IntVar(),
            "overflow": tk.IntVar(),
            "carry": tk.IntVar(),
            "zero": tk.IntVar(),
        }

        tk.Label(self, text="Name", relief=tk.RIDGE, width=12).grid(row=0, column=0)
        tk.Label(self, text="Value", relief=tk.RIDGE, width=12).grid(row=0, column=1)

        for i, name in enumerate(self.vars):
            tk.Label(self, text=name, relief=tk.RIDGE, width=12).grid(row=i + 1, column=0)
            tk.Checkbutton(
                self,
                variable=self.vars[name],
                onvalue=1,
                offvalue=0,
                command=functools.partial(self._on_toggle, flag=name),
            ).grid(row=i + 1, column=1)

        self.refresh()

    def _on_toggle(self, flag: str) -> None:
        setattr(self.alu, flag, bool(self.vars[flag].get()))

    def refresh(self) -> None:
        for name, var in self.vars.items():
            var.set(int(getattr(self.alu, name)))
