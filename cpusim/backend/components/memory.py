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
from cpusim.common.types import Int16

__all__ = ["Memory"]


class Memory:
    __slots__ = ("_data",)

    def __init__(self, initial_data: list[int], max_size: int = 4096) -> None:
        data = list(initial_data)
        self._data: list[Int16] = [Int16(v) for v in data[:max_size]]
        if len(data) < max_size:
            self._data.extend([Int16(0) for _ in range(max_size - len(data))])

    def get(self, address: int) -> Int16:
        if address >= len(self._data):
            raise ValueError("Address out of bounds")

        return self._data[address]

    def set(self, address: int, value: Int16) -> None:
        if address >= len(self._data):
            raise ValueError("Address out of bounds")

        self._data[address] = value
