from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class GreaterEquals(tc.Formula):
    """
    A class representing the comparison '>='.
    """

    @typechecked
    def __init__(
        self,
        left: tuple[tc.Variable, str] | tc.PRIMITIVE_TYPES,
        right: tuple[tc.Variable, str] | tc.PRIMITIVE_TYPES,
    ) -> None:
        """
        Parameters
        ----------
        left : tuple[Variable, str] | PRIMITIVE_TYPES (such as str, int, float)
            Left-hand side of the comparison.
        right : tuple[Variable, str] | PRIMITIVE_TYPES (such as str, int, float)
            Right-hand side of the comparison.
        """
        super().__init__([])
        self.left = left
        self.right = right

    @typechecked
    def __deepcopy__(self, memo) -> GreaterEquals:
        return GreaterEquals(deepcopy(self.left, memo), deepcopy(self.right, memo))

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.left, tuple):  # (variable, attr_name)
            left_string = f"\\text{{{self.left[0].name}.{self.left[1]}}}"
        else:
            left_string = f"\\text{{{self.left}}}"
        if isinstance(self.right, tuple):  # (variable, attr_name)
            right_string = f"\\text{{{self.right[0].name}.{self.right[1]}}}"
        else:
            right_string = f"\\text{{{self.right}}}"
        return f"{left_string} >= {right_string}"

    @typechecked
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, GreaterEquals)
            and self.left == other.left
            and self.right == other.right
        )

    @typechecked
    def expand_quantifiers(self) -> tc.Formula:
        return self

    @typechecked
    def move_quantifiers_inwards(self) -> tc.Formula:
        return self

    @typechecked
    def _move_same_type_quantifiers_outwards(
        self, move_exists: bool, move_forall: bool
    ) -> tc.Formula:
        return self

    @typechecked
    def _to_sql(self) -> str:
        if isinstance(self.left, tuple):  # (variable, attr_name)
            left_string = f"{self.left[0].name}.{self.left[1]}"
        else:
            left_string = f"{self.left}"
        if isinstance(self.right, tuple):  # (variable, attr_name)
            right_string = f"{self.right[0].name}.{self.right[1]}"
        else:
            right_string = f"{self.right}"
        return f"{left_string} >= {right_string}"

    @typechecked
    def flatten_quantifiers(self) -> tc.Formula:
        return self

    @typechecked
    def _to_normal_form(self) -> tc.Formula:
        return self

    @typechecked
    def contains_variable(self, variable: tc.Variable) -> bool:
        return (isinstance(self.left, tuple) and self.left[0] == variable) or (
            isinstance(self.right, tuple) and self.right[0] == variable
        )

    @typechecked
    def contains_variable_typing(self, variable: tc.Variable) -> bool:
        return False

    @typechecked
    def _rename_variable(
        self, old_variable: tc.Variable, new_variable: tc.Variable
    ) -> tc.Formula:
        if isinstance(self.left, tuple) and self.left[0] == old_variable:
            self.left = (new_variable, self.left[1])
        if isinstance(self.right, tuple) and self.right[0] == old_variable:
            self.right = (new_variable, self.right[1])
        return self

    @typechecked
    def _prune_variable_atoms(self) -> tc.Formula | None:
        return self

    @typechecked
    def get_used_variables(self) -> set[tc.Variable]:
        variables = set()

        if isinstance(self.left, tuple):
            variables.add(self.left[0])

        if isinstance(self.right, tuple):
            variables.add(self.right[0])

        return variables

    @typechecked
    def _check_variable_legality(self, variable: tc.Variable) -> bool:
        return True
