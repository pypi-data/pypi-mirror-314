from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

from typing import Any, Optional

import relational_calculus.domain_calculus as dc


class Not(dc.Formula):
    @typechecked
    def __init__(self, child: dc.Formula) -> None:
        super().__init__([child])

    @typechecked
    def __deepcopy__(self, memo) -> Not:
        return Not(deepcopy(self.children[0], memo))

    @typechecked
    def __repr__(self) -> str:
        if isinstance(
            self.children[0],
            dc.And
            | dc.Or
            | dc.Equals
            | dc.GreaterEquals
            | dc.LessEquals
            | dc.GreaterThan
            | dc.LessThan,
        ):
            return f"\\neg({self.children[0]})"
        return f"\\neg {self.children[0]}"

    @typechecked
    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Not) and self.children[0] == other.children[0]

    @typechecked
    def _to_sql(self) -> Optional[str]:
        return f"(NOT {self.children[0].to_sql()})"

    @typechecked
    def _to_normal_form(self) -> dc.Formula:
        if isinstance(self.children[0], Not):
            return self.children[0].children[0]._to_normal_form()

        if isinstance(self.children[0], dc.And):
            return dc.Or(
                Not(self.children[0].children[0]), Not(self.children[0].children[1])
            )._to_normal_form()

        if isinstance(self.children[0], dc.Or):
            return dc.And(
                Not(self.children[0].children[0]), Not(self.children[0].children[1])
            )._to_normal_form()

        if isinstance(self.children[0], dc.Exists):
            return dc.Forall(
                self.children[0].variable, Not(self.children[0].children[0])
            )._to_normal_form()

        if isinstance(self.children[0], dc.Forall):
            return dc.Exists(
                self.children[0].variable, Not(self.children[0].children[0])
            )._to_normal_form()

        # if nothing changed, then convert child
        return Not(self.children[0]._to_normal_form())

    @typechecked
    def contains_variable(self, variable: dc.Variable) -> bool:
        return self.children[0].contains_variable(variable)

    @typechecked
    def contains_variable_typing(self, variable: dc.Variable) -> bool:
        return self.children[0].contains_variable_typing(variable)

    @typechecked
    def contains_variable_quantification(self, variable: dc.Variable) -> bool:
        return self.children[0].contains_variable_quantification(variable)

    @typechecked
    def _rename_variable(
        self, variable: dc.Variable, new_variable: dc.Variable
    ) -> dc.Formula:
        return Not(self.children[0]._rename_variable(variable, new_variable))

    @typechecked
    def _prune_tuple_atoms(self) -> dc.Formula | None:
        new_child = self.children[0]._prune_tuple_atoms()
        if new_child is None:
            return None

        return Not(new_child)

    @typechecked
    def get_used_variables(self) -> set[dc.Variable]:
        return self.children[0].get_used_variables()

    @typechecked
    def get_used_tuples(self) -> set[dc.Tuple]:
        return self.children[0].get_used_tuples()

    @typechecked
    def _check_variable_legality(self, variable: dc.Variable) -> bool:
        if self.children[0].contains_variable_typing(variable):
            # reminder: we are in Normal Form
            raise Exception("Eine Variablendeklaration kann nicht negiert werden")

        return self.children[0]._check_variable_legality(variable)
