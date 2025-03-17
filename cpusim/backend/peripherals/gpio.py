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

import typing as t

from cpusim.common.types import Int16

if t.TYPE_CHECKING:
    from cpusim.backend import simulators


class GPIOConfig(t.NamedTuple):
    ports: int
    map_to: int


DEFAULT_CONFIG = GPIOConfig(2, 0xFC)


class GPIO:
    __slots__ = ("_cpu", "_cfg", "devices")

    def __init__(self, cpu: simulators.CPU[t.Any], cfg: GPIOConfig = DEFAULT_CONFIG) -> None:
        self._cpu = cpu
        cpu.memory.memmap("gpio", list(range(cfg.map_to, cfg.map_to + (2 * cfg.ports))), self.on_read, self.on_write)

        self._cfg = cfg

        self.devices: list[None] = [None for _ in range(cfg.ports)]

    def on_read(self, address: int) -> Int16:
        ...

    def on_write(self, address: int, val: Int16) -> None:
        ...
