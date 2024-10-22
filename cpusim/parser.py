# -*- coding: utf-8 -*-
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
from cpusim.instructions.base import Instruction

_OPCODE_REPRS: dict[int, str] = {
    0b0000: "move",
    0b0001: "add",
    0b0010: "sub",
    0b0011: "and",
    0b0100: "load",
    0b0101: "store",
    0b0110: "addm",
    0b0111: "subm",
    0b1000: "jump",
    0b1001: "jumpz",
    0b1010: "jumpnz",
    0b1011: "jumpc",
    0b1100: "call",
}

def opcode_repr(op: int) -> str:
    if op in _OPCODE_REPRS:
        return _OPCODE_REPRS[op]

    # TODO - 0b1111 + (...) opcodes
    return "unknown instruction"


def parse_dat_file(content: bytes) -> list[Instruction]:
    ...
