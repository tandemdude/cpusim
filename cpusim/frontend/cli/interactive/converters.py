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
import dataclasses
import re

_dec_hex_bin = r"\d+|0x[0-9a-f]+|0b[01]+"
_reg = r"r[a-z]|pc|acc|ir"
_REGISTER_OR_ADDR = re.compile(rf"(?P<addr>{_dec_hex_bin})|(?P<reg>{_reg})")


@dataclasses.dataclass(slots=True)
class Address:
    value: int


@dataclasses.dataclass(slots=True)
class Register:
    attr_name: str
    register_name: str
    id: int


def number_string_to_int(number_string: str) -> int:
    if number_string.startswith("0x"):
        return int(number_string, 16)
    elif number_string.startswith("0b"):
        return int(number_string, 2)
    return int(number_string)


def parse_address_or_register(s: str) -> Address | Register:
    if (match := _REGISTER_OR_ADDR.fullmatch(s)) is None:
        raise ValueError(f"could not parse address or register name from '{s}'")

    if (addr := match.group("addr")) is not None:
        return Address(number_string_to_int(addr))

    reg = match.group("reg")
    assert reg is not None

    reg_id = -1 if not reg.startswith("r") else (ord(reg[1]) - ord("a"))
    return Register("registers" if reg.startswith("r") else reg, reg, reg_id)
