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

import abc
import typing as t

from cpusim.common.types import Int16

if t.TYPE_CHECKING:
    from cpusim.backend import simulators


class GPIODevice(abc.ABC):
    __slots__ = ()

    @abc.abstractmethod
    def on_gpio_read(self, offset: t.Literal[0, 1]) -> Int16: ...

    @abc.abstractmethod
    def on_gpio_write(self, offset: t.Literal[0, 1], val: Int16) -> None: ...


class GPIOConfig(t.NamedTuple):
    ports: int
    map_to: int


DEFAULT_CONFIG = GPIOConfig(2, 0xFC)


class GPIO:
    __slots__ = ("_cfg", "_cpu", "_devices")

    def __init__(self, cpu: simulators.CPU[t.Any], cfg: GPIOConfig = DEFAULT_CONFIG) -> None:
        self._cpu = cpu
        cpu.memory.memmap("gpio", list(range(cfg.map_to, cfg.map_to + (2 * cfg.ports))), self.on_read, self.on_write)
        self._cfg = cfg

        self._devices: list[GPIODevice | None] = [None for _ in range(cfg.ports)]

    def set_device(self, port: int, device: GPIODevice | None) -> None:
        self._devices[port] = device

    def on_read(self, address: int) -> Int16:
        port, offset = (rel := (address - self._cfg.map_to)) // 2, rel % 2
        if (device := self._devices[port]) is None:
            return Int16(0)

        return device.on_gpio_read(offset)  # type: ignore[reportArgumentType]

    def on_write(self, address: int, val: Int16) -> None:
        port, offset = (rel := (address - self._cfg.map_to)) // 2, rel % 2
        if (device := self._devices[port]) is None:
            return

        device.on_gpio_write(offset, val)  # type: ignore[reportArgumentType]


class BugTrap(GPIODevice):
    __slots__ = (
        "fire_button_pressed",
        "led_on",
        "mode_switch_manual",
        "sensor_1_triggered",
        "sensor_2_triggered",
        "trap_closed",
    )

    def __init__(self) -> None:
        self.sensor_1_triggered = False
        self.sensor_2_triggered = False
        self.mode_switch_manual = False
        self.fire_button_pressed = False

        self.trap_closed = False
        self.led_on = False

    def on_gpio_read(self, offset: t.Literal[0, 1]) -> Int16:
        if offset == 1:
            return Int16(0)

        return Int16(
            0  # TODO - OSC ?
            + (int(self.mode_switch_manual) << 3)
            + (int(self.sensor_2_triggered) << 2)
            + (int(self.sensor_1_triggered) << 1)
            + (int(self.fire_button_pressed))
        )

    def on_gpio_write(self, offset: t.Literal[0, 1], val: Int16) -> None:
        if offset == 1:
            return

        self.trap_closed = bool(val.unsigned_value & 0b1)
        self.led_on = bool(val.unsigned_value & 0b10)
