from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

from typing import Any, Optional

import relational_calculus.domain_calculus as dc


class LessThan(dc.Formula):
    @typechecked
    def __init__(
        self,
        left: dc.PRIMITIVE_TYPES | dc.Variable,
        right: dc.PRIMITIVE_TYPES | dc.Variable,
    ) -> None:
        super().__init__([])
        self.left = left
        self.right = right

    @typechecked
    def __deepcopy__(self, memo) -> LessThan:
        return LessThan(deepcopy(self.left, memo), deepcopy(self.right, memo))

    @typechecked
    def __repr__(self) -> str:
        return f"{self.left} < {self.right}"

    @typechecked
    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, LessThan)
            and self.left == other.left
            and self.right == other.right
        )

    @typechecked
    def _to_sql(self) -> Optional[str]:
        if isinstance(self.left, dc.Variable):
            left_string = f'"{self.left.name}"'
        else:
            left_string = f"{str(self.left)}"
        if isinstance(self.right, dc.Variable):
            right_string = f'"{self.right.name}"'
        else:
            right_string = f"{str(self.right)}"

        return f"{left_string} < {right_string}"

    @typechecked
    def _to_normal_form(self) -> dc.Formula:
        return self

    @typechecked
    def contains_variable(self, variable: dc.Variable) -> bool:
        return self.left == variable or self.right == variable

    @typechecked
    def contains_variable_typing(self, variable: dc.Variable) -> bool:
        return False

    @typechecked
    def contains_variable_quantification(self, variable: dc.Variable) -> bool:
        return False

    @typechecked
    def _rename_variable(
        self, old_variable: dc.Variable, new_variable: dc.Variable
    ) -> dc.Formula:
        if self.left == old_variable:
            self.left = new_variable
        if self.right == old_variable:
            self.right = new_variable
        return self

    @typechecked
    def _prune_tuple_atoms(self) -> dc.Formula | None:
        return self

    @typechecked
    def get_used_variables(self) -> set[dc.Variable]:
        variables = set()

        if isinstance(self.left, dc.Variable):
            variables.add(self.left)

        if isinstance(self.right, dc.Variable):
            variables.add(self.right)

        return variables

    @typechecked
    def get_used_tuples(self) -> set[dc.Tuple]:
        return set()

    @typechecked
    def _check_variable_legality(self, variable: dc.Variable) -> bool:
        return True
