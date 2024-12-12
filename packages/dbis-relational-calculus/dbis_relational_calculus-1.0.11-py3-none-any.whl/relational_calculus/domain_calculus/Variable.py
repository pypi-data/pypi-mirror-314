from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.domain_calculus as dc


class Variable:
    @typechecked
    def __init__(self, name: str) -> None:
        self.name = name.lower()

    @typechecked
    def __copy__(self) -> Variable:
        return deepcopy(self)

    @typechecked
    def __deepcopy__(self, memo) -> Variable:
        return Variable(deepcopy(self.name, memo))

    @typechecked
    def __repr__(self) -> str:
        return f"\\text{{{self.name}}}"

    @typechecked
    def __eq__(self, other) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    @typechecked
    def __hash__(self) -> int:
        return hash(self.name)
