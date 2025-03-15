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
from cpusim.common.instructions.v1a import primary as primary_1a
from cpusim.common.instructions.v1d import primary as primary_1d
from cpusim.common.instructions.v1d import secondary as secondary_1d

__all__ = ["INSTRUCTION_SET_1A", "INSTRUCTION_SET_1D"]

INSTRUCTION_SET_1A = {
    0b0000: primary_1a.Move(),
    0b0001: primary_1a.Add(),
    0b0010: primary_1a.Sub(),
    0b0011: primary_1a.And(),
    0b0100: primary_1a.Load(),
    0b0101: primary_1a.Store(),
    0b0110: primary_1a.AddM(),
    0b0111: primary_1a.SubM(),
    0b1000: primary_1a.JumpU(),
    0b1001: primary_1a.JumpZ(),
    0b1010: primary_1a.JumpNZ(),
}

INSTRUCTION_SET_1D = {
    (0b0000, -1): primary_1d.Move(),
    (0b0001, -1): primary_1d.Add(),
    (0b0010, -1): primary_1d.Sub(),
    (0b0011, -1): primary_1d.And(),
    (0b0100, -1): primary_1d.Load(),
    (0b0101, -1): primary_1d.Store(),
    (0b0110, -1): primary_1d.AddM(),
    (0b0111, -1): primary_1d.SubM(),
    (0b1000, -1): primary_1d.JumpU(),
    (0b1001, -1): primary_1d.JumpZ(),
    (0b1010, -1): primary_1d.JumpNZ(),
    (0b1011, -1): primary_1d.JumpC(),
    (0b1100, -1): primary_1d.Call(),
    (0b1101, -1): primary_1d.Or(),
    (0b1110, -1): primary_1d.Xop1(),
    (0b1111, 0b0000): secondary_1d.Ret(),
    (0b1111, 0b0001): secondary_1d.Move(),
    (0b1111, 0b0010): secondary_1d.Load(),
    (0b1111, 0b0011): secondary_1d.Store(),
    (0b1111, 0b0100): secondary_1d.Rol(),
    (0b1111, 0b0101): secondary_1d.Ror(),
    (0b1111, 0b0110): secondary_1d.Add(),
    (0b1111, 0b0111): secondary_1d.Sub(),
    (0b1111, 0b1000): secondary_1d.And(),
    (0b1111, 0b1001): secondary_1d.Or(),
    (0b1111, 0b1010): secondary_1d.Xor(),
    (0b1111, 0b1011): secondary_1d.Asl(),
    (0b1111, 0b1100): secondary_1d.Xop2(),
    (0b1111, 0b1101): secondary_1d.Xop3(),
    (0b1111, 0b1110): secondary_1d.Xop4(),
    (0b1111, 0b1111): secondary_1d.Xop5(),
}
