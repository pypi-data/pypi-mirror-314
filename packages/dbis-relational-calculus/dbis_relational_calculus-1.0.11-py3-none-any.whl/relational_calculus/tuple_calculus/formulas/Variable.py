from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class Variable(tc.Formula):
    """
    This class represents a variable of in tuple calculus, while technically also serving as an atom.
    """

    @typechecked
    def __init__(self, name: str, type: str) -> None:
        """
        Parameters
        ----------
        name : str
            The name of the variable.
        type : str
            The relation / type that this variable is of.
        """
        super().__init__([])
        self.name = name.lower()
        self.type = type.upper()

    @typechecked
    def __deepcopy__(self, memo) -> Variable:
        return Variable(deepcopy(self.name, memo), deepcopy(self.type, memo))

    @typechecked
    def __repr__(self) -> str:
        return f"\\text{{{self.name}}} \\in \\text{{{self.type}}}"

    @typechecked
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Variable)
            and self.name == other.name
            and self.type == other.type
        )

    @typechecked
    def __hash__(self) -> int:
        return hash((self.name, self.type))

    @typechecked
    def _to_sql(self) -> str:
        raise Exception("Internal Error: Das sollte nicht passieren!")

    @typechecked
    def _to_normal_form(self) -> tc.Formula:
        return self

    @typechecked
    def contains_variable(self, variable: tc.Variable) -> bool:
        return self == variable

    @typechecked
    def contains_variable_typing(self, variable: tc.Variable) -> bool:
        return self == variable

    @typechecked
    def _rename_variable(
        self, old_variable: tc.Variable, new_variable: tc.Variable
    ) -> tc.Formula:
        if self == old_variable:
            raise Exception("Internal Error")
        return self

    @typechecked
    def _prune_variable_atoms(self) -> tc.Formula | None:
        return None

    @typechecked
    def get_used_variables(self) -> set[tc.Variable]:
        return {self}

    @typechecked
    def _check_variable_legality(self, variable: tc.Variable) -> bool:
        return True

    @typechecked
    def __getitem__(self, attribute: str) -> tuple[Variable, str]:
        return self, attribute
