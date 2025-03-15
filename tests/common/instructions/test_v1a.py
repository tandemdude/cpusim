import pytest

from cpusim.backend import simulators
from cpusim.common.instructions.v1a import primary
from cpusim.common.types import Int8
from cpusim.common.types import Int16


@pytest.fixture
def cpu() -> simulators.CPU1a:
    return simulators.CPU1a()


def test_move(cpu: simulators.CPU1a) -> None:
    primary.Move().execute((0, 15), cpu)
    assert cpu.acc.value == 15


def test_add(cpu: simulators.CPU1a) -> None:
    primary.Add().execute((0, 15), cpu)
    assert cpu.acc.value == 15


def test_sub(cpu: simulators.CPU1a) -> None:
    primary.Sub().execute((0, 15), cpu)
    assert Int8(cpu.acc.value).signed_value == -15


def test_and(cpu: simulators.CPU1a) -> None:
    cpu.acc.set(0xFF)
    primary.And().execute((0, 0), cpu)
    assert cpu.acc.value == 0


def test_load(cpu: simulators.CPU1a) -> None:
    cpu.memory.set(1, Int16(0x0023))
    primary.Load().execute((1,), cpu)
    assert cpu.acc.value == 0x23


def test_store(cpu: simulators.CPU1a) -> None:
    cpu.acc.set(0x12)
    primary.Store().execute((3,), cpu)
    assert cpu.memory.get(3).unsigned_value == 0x0012


def test_addm(cpu: simulators.CPU1a) -> None:
    cpu.memory.set(1, Int16(0x0023))
    primary.AddM().execute((1,), cpu)
    assert cpu.acc.value == 0x23


def test_subm(cpu: simulators.CPU1a) -> None:
    cpu.memory.set(1, Int16(5))
    primary.SubM().execute((1,), cpu)
    assert Int8(cpu.acc.value).signed_value == -5


def test_jumpu(cpu: simulators.CPU1a) -> None:
    primary.JumpU().execute((25,), cpu)
    assert cpu.pc.value == 25


def test_jumpz(cpu: simulators.CPU1a) -> None:
    cpu.alu.zero = False
    primary.JumpZ().execute((25,), cpu)
    assert cpu.pc.value == 0

    cpu.pc.set(0)

    cpu.alu.zero = True
    primary.JumpZ().execute((25,), cpu)
    assert cpu.pc.value == 25


def test_jumpnz(cpu: simulators.CPU1a) -> None:
    cpu.alu.zero = False
    primary.JumpNZ().execute((25,), cpu)
    assert cpu.pc.value == 25

    cpu.pc.set(0)

    cpu.alu.zero = True
    primary.JumpNZ().execute((25,), cpu)
    assert cpu.pc.value == 0
