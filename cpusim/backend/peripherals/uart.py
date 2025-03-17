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
import typing as t

from cpusim.common.types import Int16

if t.TYPE_CHECKING:
    from cpusim.backend import simulators


class UARTConfig(t.NamedTuple):
    word_0: int
    word_1: int


DEFAULT_CONFIG = UARTConfig(0xFFE, 0xFFF)


class UART:
    __slots__ = ("_cpu", "_cfg", "tx_idle", "rx_idle", "rx_data_valid", "rx_data", "tx_data_0", "tx_data_1")

    def __init__(self, cpu: simulators.CPU[t.Any], cfg: UARTConfig = DEFAULT_CONFIG) -> None:
        self._cpu = cpu
        cpu.memory.memmap("uart", [cfg.word_0, cfg.word_1], self.on_read, self.on_write)

        self._cfg = cfg

        # status bits
        self.tx_idle = 1
        self.rx_idle = 1
        self.rx_data_valid = 1
        # uart data
        self.rx_data = Int16(0)
        self.tx_data_0 = Int16(0)
        self.tx_data_1 = Int16(0)

    @property
    def _status(self) -> Int16:
        return Int16(self.tx_idle << 2 | self.rx_idle << 1 | self.rx_data_valid)

    def on_read(self, address: int) -> Int16:
        if address == 0xFFE:
            return self._status

        self.rx_data_valid = 0
        return self.rx_data

    def on_write(self, address: int, val: Int16) -> None: ...
