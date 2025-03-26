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
from tkinter import ttk


class EntryPopup(ttk.Entry):
    def __init__(self, parent: EditableTreeView, iid: str, text: str, **kwargs: t.Any) -> None:
        ttk.Style().configure("pad.TEntry", padding="1 1 1 1")
        super().__init__(parent, style="pad.TEntry", **kwargs)

        self._parent = parent
        self._iid = iid
        self.insert(0, text)

        self["exportselection"] = False

        self.focus_force()
        self.select_all()
        self.bind("<Return>", self.on_return)
        self.bind("<Control-a>", lambda *_: self.select_all())
        self.bind("<Escape>", lambda *_: self.destroy())

    def on_return(self, _: tk.Event[t.Any]) -> None:
        self._parent.on_edit_fn(self._iid, self.get())
        self.destroy()

    def select_all(self) -> str:
        self.selection_range(0, "end")
        return "break"


class EditableTreeView(ttk.Treeview):
    def __init__(
        self,
        col: str,
        col_idx: int,
        on_edit_fn: t.Callable[[str, str], None],
        *args: t.Any,
        exclude_iids: tuple[str] = (),
        **kwargs: t.Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.bind("<Double-1>", self.on_double_click)

        self.col = col
        self.col_idx = col_idx
        self.on_edit_fn = on_edit_fn
        self.exclude_iids = exclude_iids

        self._entry_popup: EntryPopup | None = None

    def on_double_click(self, event: tk.Event[t.Any]) -> None:
        if self._entry_popup is not None:
            self._entry_popup.destroy()

        rowid = self.identify_row(event.y)
        if rowid in self.exclude_iids:
            return

        column = self.col

        if not rowid:
            return

        x, y, width, height = self.bbox(rowid, column)
        pady = height // 2

        self._entry_popup = EntryPopup(self, rowid, self.item(rowid, "values")[self.col_idx])
        self._entry_popup.place(x=x, y=y + pady, width=width, height=height, anchor="w")
