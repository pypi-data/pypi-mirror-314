from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

from typing import Any, Optional

import relational_calculus.domain_calculus as dc


class Or(dc.Formula):
    @typechecked
    def __init__(self, child1: dc.Formula, child2: dc.Formula) -> None:
        super().__init__([child1, child2])

    @typechecked
    def __deepcopy__(self, memo) -> Or:
        return Or(deepcopy(self.children[0], memo), deepcopy(self.children[1], memo))

    @typechecked
    def __repr__(self) -> str:
        left = self.children[0]
        right = self.children[1]

        if isinstance(self.children[0], Or):
            left_grandchild = self.children[0].children[0]
            right_grandchild = self.children[0].children[1]
            left_repr = f"{left_grandchild}"
            right_repr = f"{right_grandchild}"
            if not isinstance(left_grandchild, Or | dc.ATOM_TYPES | dc.Tuple):
                left_repr = f"({left_repr})"
            if not isinstance(right_grandchild, Or | dc.ATOM_TYPES | dc.Tuple):
                right_repr = f"({right_repr})"
            left = f"{left_repr} \\land {right_repr}"
        elif not isinstance(self.children[0], dc.Not | dc.ATOM_TYPES | dc.Tuple):
            left = f"({left})"

        if isinstance(self.children[1], Or):
            left_grandchild = self.children[1].children[0]
            right_grandchild = self.children[1].children[1]
            left_repr = f"{left_grandchild}"
            right_repr = f"{right_grandchild}"
            if not isinstance(left_grandchild, Or | dc.ATOM_TYPES | dc.Tuple):
                left_repr = f"({left_repr})"
            if not isinstance(right_grandchild, Or | dc.ATOM_TYPES | dc.Tuple):
                right_repr = f"({right_repr})"
            right = f"{left_repr} \\land {right_repr}"
        elif not isinstance(self.children[1], dc.Not | dc.ATOM_TYPES | dc.Tuple):
            right = f"({right})"

        return f"{left} \\lor {right}"

    @typechecked
    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Or)
            and self.children[0] == other.children[0]
            and self.children[1] == other.children[1]
        )

    @typechecked
    def _to_sql(self) -> Optional[str]:
        return f"({self.children[0].to_sql()} OR {self.children[1].to_sql()})"

    @typechecked
    def _to_normal_form(self) -> dc.Formula:
        if isinstance(self.children[0], dc.Exists):
            self.children[0] = self.children[0]._to_normal_form()
            variable = self.children[0].variable
            if self.children[1].contains_variable(variable):
                return Or(
                    self.children[0].rename_variable(variable), self.children[1]
                )._to_normal_form()
            else:
                return dc.Exists(
                    variable,
                    Or(
                        self.children[0].children[0], self.children[1]
                    )._to_normal_form(),
                )

        if isinstance(self.children[0], dc.Forall):
            self.children[0] = self.children[0]._to_normal_form()
            variable = self.children[0].variable
            if self.children[1].contains_variable(variable):
                return Or(
                    self.children[0].rename_variable(variable), self.children[1]
                )._to_normal_form()
            else:
                return dc.Forall(
                    variable,
                    Or(
                        self.children[0].children[0], self.children[1]
                    )._to_normal_form(),
                )

        if isinstance(self.children[1], dc.Exists):
            self.children[1] = self.children[1]._to_normal_form()
            variable = self.children[1].variable
            if self.children[0].contains_variable(variable):
                return Or(
                    self.children[0], self.children[1].rename_variable(variable)
                )._to_normal_form()
            else:
                return dc.Exists(
                    variable,
                    Or(
                        self.children[0], self.children[1].children[0]
                    )._to_normal_form(),
                )

        if isinstance(self.children[1], dc.Forall):
            self.children[1] = self.children[1]._to_normal_form()
            variable = self.children[1].variable
            if self.children[0].contains_variable(variable):
                return Or(
                    self.children[0], self.children[1].rename_variable(variable)
                )._to_normal_form()
            else:
                return dc.Forall(
                    variable,
                    Or(
                        self.children[0], self.children[1].children[0]
                    )._to_normal_form(),
                )

        return Or(
            self.children[0]._to_normal_form(), self.children[1]._to_normal_form()
        )

    @typechecked
    def contains_variable(self, variable: dc.Variable) -> bool:
        return self.children[0].contains_variable(variable) or self.children[
            1
        ].contains_variable(variable)

    @typechecked
    def contains_variable_typing(self, variable: dc.Variable) -> bool:
        return self.children[0].contains_variable_typing(variable) or self.children[
            1
        ].contains_variable_typing(variable)

    @typechecked
    def contains_variable_quantification(self, variable: dc.Variable) -> bool:
        return self.children[0].contains_variable_quantification(
            variable
        ) or self.children[1].contains_variable_quantification(variable)

    @typechecked
    def _rename_variable(
        self, old_variable: dc.Variable, new_variable: dc.Variable
    ) -> dc.Formula:
        return Or(
            self.children[0]._rename_variable(old_variable, new_variable),
            self.children[1]._rename_variable(old_variable, new_variable),
        )

    @typechecked
    def _prune_tuple_atoms(self) -> dc.Formula | None:
        left = self.children[0]._prune_tuple_atoms()
        right = self.children[1]._prune_tuple_atoms()

        if left is None and right is None:
            return None
        elif left is None:
            return right
        elif right is None:
            return left
        else:
            return Or(left, right)

    @typechecked
    def get_used_variables(self) -> set[dc.Variable]:
        return (
            self.children[0]
            .get_used_variables()
            .union(self.children[1].get_used_variables())
        )

    @typechecked
    def get_used_tuples(self) -> set[dc.Tuple]:
        return (
            self.children[0].get_used_tuples().union(self.children[1].get_used_tuples())
        )

    @typechecked
    def _check_variable_legality(self, variable: dc.Variable) -> bool:
        if self.children[0].contains_variable_quantification(
            variable
        ) and self.children[1].contains_variable_quantification(variable):
            # cannot happen due to renaming of variables
            raise Exception("Internal Error")

        if self.children[0].contains_variable_quantification(
            variable
        ) and self.children[1].contains_variable(variable):
            raise Exception("Jede Variable muss vor der Nutzung deklariert sein")

        if self.children[0].contains_variable(variable) and self.children[
            1
        ].contains_variable_quantification(variable):
            raise Exception("Jede Variable muss vor der Nutzung deklariert sein")

        return self.children[0]._check_variable_legality(variable) and self.children[
            1
        ]._check_variable_legality(variable)
