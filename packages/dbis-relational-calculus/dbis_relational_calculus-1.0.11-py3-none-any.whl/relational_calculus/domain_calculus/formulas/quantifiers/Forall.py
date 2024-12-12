from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

from typing import Any, Optional

import relational_calculus.domain_calculus as dc


class Forall(dc.Formula):
    @typechecked
    def __init__(
        self, variable: dc.Variable | set[dc.Variable], child: dc.Formula
    ) -> None:
        super().__init__([child])
        self.variable = variable
        if isinstance(self.variable, set) and len(self.variable) == 0:
            raise Exception("Mindestens eine Variable muss quantifiziert werden")

    @typechecked
    def __deepcopy__(self, memo) -> Forall:
        return Forall(deepcopy(self.variable, memo), deepcopy(self.children[0], memo))

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.variable, set):
            forall_str = ""
            for var in self.variable:
                forall_str += f"{var.name}, "
            forall_str = forall_str[: -len(", ")]
        else:
            forall_str = self.variable.name

        return f"\\forall_{{{forall_str}}}({self.children[0]})"

    @typechecked
    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Forall)
            and self.variable == other.variable
            and self.children[0] == other.children[0]
        )

    @typechecked
    def _to_sql(self) -> Optional[str]:
        return None

    @typechecked
    def _to_normal_form(self) -> dc.Formula:
        if isinstance(self.variable, set):
            formula = self.children[0]._to_normal_form()
            for var in self.variable:
                formula = Forall(var, formula)
            return formula
        return Forall(self.variable, self.children[0]._to_normal_form())

    @typechecked
    def contains_variable(self, variable: dc.Variable) -> bool:
        return (
            variable in self.variable
            if isinstance(self.variable, set)
            else self.variable == variable
        ) or self.children[0].contains_variable(variable)

    @typechecked
    def contains_variable_typing(self, variable: dc.Variable) -> bool:
        return False

    @typechecked
    def contains_variable_quantification(self, variable: dc.Variable) -> bool:
        return self.contains_variable(variable) or self.children[
            0
        ].contains_variable_quantification(variable)

    @typechecked
    def _rename_variable(
        self, old_variable: dc.Variable, new_variable: dc.Variable
    ) -> dc.Formula:
        if isinstance(self.variable, set):
            new_set = set(self.variable)
            if old_variable in self.variable:
                new_set.remove(old_variable)
                new_set.add(new_variable)
            return Forall(
                new_set, self.children[0]._rename_variable(old_variable, new_variable)
            )
        else:
            if self.variable == old_variable:
                return Forall(new_variable, self.children[0])
            else:
                return Forall(
                    new_variable,
                    self.children[0]._rename_variable(old_variable, new_variable),
                )

    @typechecked
    def _prune_tuple_atoms(self) -> dc.Formula | None:
        new_child = self.children[0]._prune_tuple_atoms()
        if new_child is None:
            return None
        if isinstance(self.variable, set):
            new_set = set(self.variable)
            for var in self.variable:
                if not new_child.contains_variable_typing(var):
                    new_set.remove(var)
            if len(new_set) == 0:
                return new_child
            return Forall(new_set, new_child)
        else:
            if not new_child.contains_variable_typing(self.variable):
                return new_child
            return Forall(self.variable, new_child)

    @typechecked
    def get_used_variables(self) -> set[dc.Variable]:
        child_vars = self.children[0].get_used_variables()
        if isinstance(self.variable, set):
            return child_vars.union(self.variable)
        return child_vars.union({self.variable})

    @typechecked
    def get_used_tuples(self) -> set[dc.Tuple]:
        return self.children[0].get_used_tuples()

    @typechecked
    def _check_variable_legality(self, variable: dc.Variable) -> bool:
        if self.variable != variable:
            return self.children[0]._check_variable_legality(variable)

        if self.children[0].contains_variable_quantification(variable):
            raise Exception(
                "Invalid input: Eine deklarierte Variable kann nicht quantifiziert werden"
            )

        return True
