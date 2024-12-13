from typing import List, Self
import inspect

from .types import Part, Face, Edge
from .step import Step


class ShapeHistory:
    def __init__(self, steps: List[Step]) -> None:
        self.steps = steps

    @staticmethod
    def from_globals(kind=Part, prefix='') -> Self:
        def filter(label: str, shape: Part) -> bool:
            return isinstance(shape, kind) and label.startswith(prefix)

        shapes = list(inspect.currentframe().f_back.f_locals.items())
        return ShapeHistory([Step(k, v) for k, v in shapes if filter(k, v)])

    def objects(self) -> List[Part]:
        return [step.object for step in self.steps]

    def labels(self) -> List[str]:
        return [step.label for step in self.steps]

    def diff(self) -> List[List[Face|Edge]]:
        previous_step = None

        for step in self.steps:
            step.colorize_faces_diff(previous_step)
            step.colorize_edges_diff(previous_step)
            previous_step = step

        return [step.get_faces_and_edges() for step in self.steps]
