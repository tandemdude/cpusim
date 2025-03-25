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


class BreakpointsFrame(tk.LabelFrame):
    def __init__(self, root: tk.Frame) -> None:
        super().__init__(root, text="Breakpoints")

        tk.Label(self, text="Type", relief=tk.RIDGE, width=12).grid(row=0, column=0)
        tk.Label(self, text="Value", relief=tk.RIDGE, width=12).grid(row=0, column=1)
        tk.Label(self, text="Enabled", relief=tk.RIDGE, width=12).grid(row=0, column=2)

        # TODO - add/remove breakpoints button

        self.refresh()

    def refresh(self) -> None: ...
