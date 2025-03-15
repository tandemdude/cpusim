import pytest

from cpusim.common.types import Int8
from cpusim.common.types import Int16


@pytest.mark.parametrize(
    ["n1", "expected_signed", "expected_unsigned"],
    [
        (Int8(0b11111111), -1, 255),
        (Int8(0b00000000), 0, 0),
        (Int8(0b10000001), -127, 129),
        (Int8(0b01111111), 127, 127),
        (Int8(0b10101010), -86, 170),
        (Int8(0b01010101), 85, 85),
    ],
)
def test_Int8_signedness(n1: Int8, expected_signed: int, expected_unsigned: int) -> None:
    assert n1.signed_value == expected_signed
    assert n1.unsigned_value == expected_unsigned


@pytest.mark.parametrize(
    ["n1", "n2", "expected"],
    [
        # simple addition without carry
        (Int8(0x01), Int8(0x01), Int8(0x02, carry=False)),
        (Int8(0x12), Int8(0x21), Int8(0x33, carry=False)),
        # maximum values without carry
        (Int8(0x7F), Int8(0x01), Int8(0x80, carry=False)),
        # addition generating carry
        (Int8(0xFF), Int8(0x01), Int8(0x00, carry=True)),
        (Int8(0x80), Int8(0x80), Int8(0x00, carry=True)),
        # adding zero
        (Int8(0x00), Int8(0x00), Int8(0x00, carry=False)),
        (Int8(0x12), Int8(0x00), Int8(0x12, carry=False)),
        # carry propagation
        (Int8(0x0F), Int8(0x01), Int8(0x10, carry=False)),
        # extra cases
        (Int8(0xFF), Int8(0xFF), Int8(0xFE, carry=True)),
        (Int8(0x7F), Int8(0x80), Int8(0xFF, carry=False)),
    ],
)
def test_Int8_unsigned_addition(n1: Int8, n2: Int8, expected: Int8) -> None:
    result = n1 + n2

    assert result.unsigned_value == expected.unsigned_value
    assert result.carry == expected.carry


@pytest.mark.parametrize(
    ["n1", "n2", "expected"],
    [
        # simple addition without overflow
        (Int8(0x01), Int8(0x01), Int8(0x02, overflow=False)),
        (Int8(0x12), Int8(0x21), Int8(0x33, overflow=False)),
        # maximum positive values without overflow
        (Int8(0x3F), Int8(0x01), Int8(0x40, overflow=False)),
        # positive overflow
        (Int8(0x7F), Int8(0x01), Int8(0x80, overflow=True)),
        # minimum negative values without overflow
        (Int8(0x81), Int8(0xFF), Int8(0x80, overflow=False)),
        # negative overflow
        (Int8(0x80), Int8(0xFF), Int8(0x7F, overflow=True)),
        # adding zero
        (Int8(0x00), Int8(0x00), Int8(0x00, overflow=False)),
        (Int8(0x12), Int8(0x00), Int8(0x12, overflow=False)),
        (Int8(0x80), Int8(0x00), Int8(0x80, overflow=False)),
        # mixed sign addition without overflow
        (Int8(0x7F), Int8(0x80), Int8(0xFF, overflow=False)),
        (Int8(0x80), Int8(0x7F), Int8(0xFF, overflow=False)),
        # extra cases
        (Int8(0x7F), Int8(0x7F), Int8(0xFE, overflow=True)),
        (Int8(0x80), Int8(0x80), Int8(0x00, overflow=True)),
    ],
)
def test_Int8_signed_addition(n1: Int8, n2: Int8, expected: Int8) -> None:
    result = n1 + n2

    assert result.signed_value == expected.signed_value
    assert result.overflow == expected.overflow


@pytest.mark.parametrize(
    ["n1", "n2", "expected"],
    [
        # simple subtraction without overflow
        (Int8(0x01), Int8(0x01), Int8(0x00, overflow=False)),
        (Int8(0x12), Int8(0x01), Int8(0x11, overflow=False)),
        (Int8(0x7F), Int8(0x7E), Int8(0x01, overflow=False)),
        # subtraction resulting in negative numbers without overflow
        (Int8(0x00), Int8(0x01), Int8(0xFF, overflow=False)),
        # negative without overflow
        (Int8(0x81), Int8(0x01), Int8(0x80, overflow=False)),
        # negative overflow
        (Int8(0x80), Int8(0x01), Int8(0x7F, overflow=True)),
        # positive overflow
        (Int8(0x7F), Int8(0xFF), Int8(0x80, overflow=True)),
        # subtraction with zero
        (Int8(0x00), Int8(0x00), Int8(0x00, overflow=False)),
        (Int8(0x12), Int8(0x00), Int8(0x12, overflow=False)),
        (Int8(0x00), Int8(0x12), Int8(0xEE, overflow=False)),
        # mixed sign subtraction
        (Int8(0x7F), Int8(0x80), Int8(0xFF, overflow=True)),
        (Int8(0x80), Int8(0x7F), Int8(0x01, overflow=True)),
        # extra cases
        (Int8(0x7F), Int8(0x7F), Int8(0x00, overflow=False)),
        (Int8(0x80), Int8(0x80), Int8(0x00, overflow=False)),
    ],
)
def test_Int8_subtraction(n1: Int8, n2: Int8, expected: Int8) -> None:
    result = n1 - n2

    assert result.signed_value == expected.signed_value
    assert result.overflow == expected.overflow


@pytest.mark.parametrize(
    ["n1", "expected_signed", "expected_unsigned"],
    [
        (Int16(0b1111111111111111), -1, 65535),
        (Int16(0b0000000000000000), 0, 0),
        (Int16(0b1000000011111111), -32513, 33023),
        (Int16(0b0000000011111111), 255, 255),
        (Int16(0b1010101010101010), -21846, 43690),
        (Int16(0b0101010101010101), 21845, 21845),
    ],
)
def test_Int16_signedness(n1: Int16, expected_signed: int, expected_unsigned: int) -> None:
    assert n1.signed_value == expected_signed
    assert n1.unsigned_value == expected_unsigned


@pytest.mark.parametrize(
    ["n1", "n2", "expected"],
    [
        # simple addition without carry
        (Int16(0x0001), Int16(0x0001), Int16(0x0002, carry=False)),
        (Int16(0x1234), Int16(0x4321), Int16(0x5555, carry=False)),
        # maximum values without carry
        (Int16(0x7FFF), Int16(0x0001), Int16(0x8000, carry=False)),
        # addition generating carry
        (Int16(0xFFFF), Int16(0x0001), Int16(0x0000, carry=True)),
        (Int16(0x8000), Int16(0x8000), Int16(0x0000, carry=True)),
        # adding zero
        (Int16(0x0000), Int16(0x0000), Int16(0x0000, carry=False)),
        (Int16(0x1234), Int16(0x0000), Int16(0x1234, carry=False)),
        # carry propagation
        (Int16(0x00FF), Int16(0x0001), Int16(0x0100, carry=False)),
        # extra cases
        (Int16(0xFFFF), Int16(0xFFFF), Int16(0xFFFE, carry=True)),
        (Int16(0x7FFF), Int16(0x8000), Int16(0xFFFF, carry=False)),
    ],
)
def test_Int16_unsigned_addition(n1: Int16, n2: Int16, expected: Int16) -> None:
    result = n1 + n2

    assert result.unsigned_value == expected.unsigned_value
    assert result.carry == expected.carry


@pytest.mark.parametrize(
    ["n1", "n2", "expected"],
    [
        # simple addition without overflow
        (Int16(0x0001), Int16(0x0001), Int16(0x0002, overflow=False)),
        (Int16(0x1234), Int16(0x4321), Int16(0x5555, overflow=False)),
        # maximum positive values without overflow
        (Int16(0x3FFF), Int16(0x0001), Int16(0x4000, overflow=False)),
        # positive overflow
        (Int16(0x7FFF), Int16(0x0001), Int16(0x8000, overflow=True)),
        # minimum negative values without overflow
        (Int16(0x8001), Int16(0xFFFF), Int16(0x8000, overflow=False)),
        # negative overflow
        (Int16(0x8000), Int16(0xFFFF), Int16(0x7FFF, overflow=True)),
        # adding zero
        (Int16(0x0000), Int16(0x0000), Int16(0x0000, overflow=False)),
        (Int16(0x1234), Int16(0x0000), Int16(0x1234, overflow=False)),
        (Int16(0x8000), Int16(0x0000), Int16(0x8000, overflow=False)),
        # mixed sign addition without overflow
        (Int16(0x7FFF), Int16(0x8000), Int16(0xFFFF, overflow=False)),
        (Int16(0x8000), Int16(0x7FFF), Int16(0xFFFF, overflow=False)),
        # extra cases
        (Int16(0x7FFF), Int16(0x7FFF), Int16(0xFFFE, overflow=True)),
        (Int16(0x8000), Int16(0x8000), Int16(0x0000, overflow=True)),
    ],
)
def test_Int16_signed_addition(n1: Int16, n2: Int16, expected: Int16) -> None:
    result = n1 + n2

    assert result.unsigned_value == expected.unsigned_value
    assert result.overflow == expected.overflow


@pytest.mark.parametrize(
    ["n1", "n2", "expected"],
    [
        # simple subtraction without overflow
        (Int16(0x0001), Int16(0x0001), Int16(0x0000, overflow=False)),  # 1 - 1 = 0
        (Int16(0x1234), Int16(0x0001), Int16(0x1233, overflow=False)),  # 4660 - 1 = 4659
        (Int16(0x7FFF), Int16(0x7FFE), Int16(0x0001, overflow=False)),  # 32767 - 32766 = 1
        # subtraction resulting in negative numbers without overflow
        (Int16(0x0000), Int16(0x0001), Int16(0xFFFF, overflow=False)),  # 0 - 1 = -1
        # negative without overflow
        (Int16(0x8001), Int16(0x0001), Int16(0x8000, overflow=False)),  # -32767 - 1 = -32768
        # negative overflow
        (Int16(0x8000), Int16(0x0001), Int16(0x7FFF, overflow=True)),  # -32768 - 1 = 32767 (overflow)
        # positive overflow
        (Int16(0x7FFF), Int16(0xFFFF), Int16(0x8000, overflow=True)),  # 32767 - (-1) = -32768 (overflow)
        # subtraction with zero
        (Int16(0x0000), Int16(0x0000), Int16(0x0000, overflow=False)),  # 0 - 0 = 0
        (Int16(0x1234), Int16(0x0000), Int16(0x1234, overflow=False)),  # 4660 - 0 = 4660
        (Int16(0x0000), Int16(0x1234), Int16(0xEDCC, overflow=False)),  # 0 - 4660 = -4660
        # mixed sign subtraction
        (Int16(0x7FFF), Int16(0x8000), Int16(0xFFFF, overflow=True)),  # 32767 - (-32768) = -1 (overflow)
        (Int16(0x8000), Int16(0x7FFF), Int16(0x0001, overflow=True)),  # -32768 - 32767 = -32769 (overflow)
        # extra cases
        (Int16(0x7FFF), Int16(0x7FFF), Int16(0x0000, overflow=False)),  # 32767 - 32767 = 0
        (Int16(0x8000), Int16(0x8000), Int16(0x0000, overflow=False)),  # -32768 - (-32768) = 0
    ],
)
def test_Int16_subtraction(n1: Int16, n2: Int16, expected: Int16) -> None:
    result = n1 - n2

    assert result.signed_value == expected.signed_value
    assert result.overflow == expected.overflow
