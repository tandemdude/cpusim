import pytest

from cpusim.backend import simulators
from cpusim.common.instructions.v1d import primary
from cpusim.common.instructions.v1d import secondary
from cpusim.common.types import Int16


@pytest.fixture
def cpu() -> simulators.CPU1d:
    return simulators.CPU1d()


def test_move(cpu: simulators.CPU1d) -> None:
    primary.Move().execute((0, 10), cpu)
    assert cpu.registers.get(0).unsigned_value == 10


def test_add(cpu: simulators.CPU1d) -> None:
    primary.Add().execute((0, 10), cpu)
    assert cpu.registers.get(0).unsigned_value == 10
    primary.Add().execute((0, 10), cpu)
    assert cpu.registers.get(0).unsigned_value == 20


def test_sub(cpu: simulators.CPU1d) -> None:
    primary.Sub().execute((0, 10), cpu)
    assert cpu.registers.get(0).signed_value == -10
    primary.Sub().execute((0, 10), cpu)
    assert cpu.registers.get(0).signed_value == -20


def test_and(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0xFFFF))
    primary.And().execute((0, 0x0F0F), cpu)
    assert cpu.registers.get(0).unsigned_value == 0x0F0F


def test_load(cpu: simulators.CPU1d) -> None:
    cpu.memory.set(1, Int16(0xBEEF))
    primary.Load().execute((1,), cpu)
    assert cpu.registers.get(0).unsigned_value == 0xBEEF


def test_store(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0xBEEF))
    primary.Store().execute((1,), cpu)
    assert cpu.memory.get(1).unsigned_value == 0xBEEF


def test_addm(cpu: simulators.CPU1d) -> None:
    cpu.memory.set(1, Int16(0xBEEF))
    primary.AddM().execute((1,), cpu)
    assert cpu.registers.get(0).unsigned_value == 0xBEEF


def test_subm(cpu: simulators.CPU1d) -> None:
    cpu.memory.set(1, Int16(25))
    primary.SubM().execute((1,), cpu)
    assert cpu.registers.get(0).signed_value == -25


def test_jumpu(cpu: simulators.CPU1d) -> None:
    primary.JumpU().execute((25,), cpu)
    assert cpu.pc.value == 25


def test_jumpz(cpu: simulators.CPU1d) -> None:
    cpu.alu.zero = False
    primary.JumpZ().execute((25,), cpu)
    assert cpu.pc.value == 0

    cpu.pc.set(0)

    cpu.alu.zero = True
    primary.JumpZ().execute((25,), cpu)
    assert cpu.pc.value == 25


def test_jumpnz(cpu: simulators.CPU1d) -> None:
    cpu.alu.zero = False
    primary.JumpNZ().execute((25,), cpu)
    assert cpu.pc.value == 25

    cpu.pc.set(0)

    cpu.alu.zero = True
    primary.JumpNZ().execute((25,), cpu)
    assert cpu.pc.value == 0


def test_jumpc(cpu: simulators.CPU1d) -> None:
    cpu.alu.carry = False
    primary.JumpC().execute((25,), cpu)
    assert cpu.pc.value == 0

    cpu.pc.set(0)

    cpu.alu.carry = True
    primary.JumpC().execute((25,), cpu)
    assert cpu.pc.value == 25


@pytest.mark.xfail
def test_call(cpu: simulators.CPU1d) -> None:
    assert False


def test_or(cpu: simulators.CPU1d) -> None:
    primary.Or().execute((0, 0xBEEF), cpu)
    assert cpu.registers.get(0).unsigned_value == 0xBEEF
    primary.Or().execute((0, 0x1234), cpu)
    assert cpu.registers.get(0).unsigned_value == (0xBEEF | 0x1234)


@pytest.mark.xfail
def test_xop1(cpu: simulators.CPU1d) -> None:
    # we expect this test to fail because xop1's behaviour is undefined
    assert False


@pytest.mark.xfail
def test_ret(cpu: simulators.CPU1d) -> None:
    assert False


def test_move_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(1, Int16(0xBEEF))
    secondary.Move().execute((0, 1), cpu)
    assert cpu.registers.get(0).unsigned_value == 0xBEEF


def test_load_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(1, Int16(2))
    cpu.memory.set(2, Int16(0xBEEF))
    secondary.Load().execute((0, 1), cpu)
    assert cpu.registers.get(0).unsigned_value == 0xBEEF


def test_store_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0xBEEF))
    cpu.registers.set(1, Int16(2))
    secondary.Store().execute((0, 1), cpu)
    assert cpu.memory.get(2).unsigned_value == 0xBEEF


def test_rol(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0b0101010101010101))
    secondary.Rol().execute((0, 0), cpu)
    assert cpu.registers.get(0).unsigned_value == 0b1010101010101010


def test_xor(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0xBEEF))
    cpu.registers.set(1, Int16(0xDEAD))
    secondary.Xor().execute((0, 1), cpu)
    assert cpu.registers.get(0).unsigned_value == (0xBEEF ^ 0xDEAD)


def test_ror(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0b1010101010101010))
    secondary.Ror().execute((0, 0), cpu)
    assert cpu.registers.get(0).unsigned_value == 0b0101010101010101


def test_add_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(5))
    cpu.registers.set(1, Int16(10))
    secondary.Add().execute((0, 1), cpu)
    assert cpu.registers.get(0).unsigned_value == 15


def test_sub_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(5))
    cpu.registers.set(1, Int16(10))
    secondary.Sub().execute((0, 1), cpu)
    assert cpu.registers.get(0).signed_value == -5


def test_and_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0xDEAD))
    cpu.registers.set(1, Int16(0xBEEF))
    secondary.And().execute((0, 1), cpu)
    assert cpu.registers.get(0).unsigned_value == (0xDEAD & 0xBEEF)


def test_or_2(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0xBEEF))
    cpu.registers.set(1, Int16(0xDEAD))
    secondary.Or().execute((0, 1), cpu)
    assert cpu.registers.get(0).unsigned_value == (0xBEEF | 0xDEAD)


def test_asl(cpu: simulators.CPU1d) -> None:
    cpu.registers.set(0, Int16(0x0001))
    secondary.Asl().execute((0, 0), cpu)
    assert cpu.registers.get(0).unsigned_value == 0x0002

    cpu.registers.set(0, Int16(0x8000))
    secondary.Asl().execute((0, 0), cpu)
    assert cpu.registers.get(0).unsigned_value == 0


@pytest.mark.xfail
def test_xop2(cpu: simulators.CPU1d) -> None:
    # we expect this test to fail because xop2's behaviour is undefined
    assert False


@pytest.mark.xfail
def test_xop3(cpu: simulators.CPU1d) -> None:
    # we expect this test to fail because xop3's behaviour is undefined
    assert False


@pytest.mark.xfail
def test_xop4(cpu: simulators.CPU1d) -> None:
    # we expect this test to fail because xop4's behaviour is undefined
    assert False


@pytest.mark.xfail
def test_xop5(cpu: simulators.CPU1d) -> None:
    # we expect this test to fail because xop5's behaviour is undefined
    assert False
