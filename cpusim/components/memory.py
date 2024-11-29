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


class Memory:
    __slots__ = ("_data",)

    def __init__(self, initial_data: list[int]) -> None:
        data = list(initial_data)
        self._data: list[int] = data[:4096]
        if len(data) < 4096:
            self._data.extend([0 for _ in range(4096 - len(data))])

    def get(self, address: int) -> int:
        if address >= len(self._data):
            raise ValueError("Address out of bounds")

        return self._data[address]

    def put(self, address: int, value: int) -> None:
        if address >= len(self._data):
            raise ValueError("Address out of bounds")

        if value > 0xFFFF:
            raise ValueError("Value out of bounds")

        self._data[address] = value
