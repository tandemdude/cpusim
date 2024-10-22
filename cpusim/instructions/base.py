import abc
import dataclasses


@dataclasses.dataclass(slots=True, frozen=True)
class InstructionData:
    opcode: int
    operands: list[int]


class Instruction(abc.ABC):
    __slots__ = ("_data",)

    def __init__(self, data: InstructionData) -> None:
        self._data = data

    @property
    def data(self) -> InstructionData:
        return self._data

    @abc.abstractmethod
    def __call__(self, *args, **kwargs) -> None:
        ...
