from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class Exists(tc.Formula):
    """
    A class representing the exists quantifier in first order logic.
    """

    @typechecked
    def __init__(
        self, variable: tc.Variable | set[tc.Variable], child: tc.Formula
    ) -> None:
        """
        Parameters
        ----------
        variable : Variable | set[Variable]
            The variable(s) that should be quantified.
        child: Formula
            The sub-formula succeding this quantifier.
        """
        super().__init__([child])
        self.variable = variable
        if isinstance(self.variable, set) and len(self.variable) == 0:
            raise Exception("Mindestens eine Variable muss quantifiziert werden")

    @typechecked
    def __deepcopy__(self, memo) -> Exists:
        return Exists(deepcopy(self.variable, memo), deepcopy(self.children[0], memo))

    @typechecked
    def __repr__(self) -> str:
        if isinstance(self.variable, set):
            forall_str = ""
            type_str = ""
            for var in self.variable:
                forall_str += f"{var.name}, "
                type_str += f"\\text{{{var.name}}} \\in \\text{{{var.type}}} \\land "
            forall_str = forall_str[: -len(", ")]
            type_str = type_str[: -len(" \\land ")]
        else:
            forall_str = self.variable.name
            type_str = (
                f"\\text{{{self.variable.name}}} \\in \\text{{{self.variable.type}}}"
            )

        return f"\\exists_{{{forall_str}}}({type_str} \\land ({self.children[0]}))"

    @typechecked
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Exists)
            and self.variable == other.variable
            and self.children[0] == other.children[0]
        )

    @typechecked
    def expand_quantifiers(self) -> tc.Formula:
        if isinstance(self.variable, set):
            formula = self.children[0].expand_quantifiers()
            for variable in self.variable:
                formula = Exists(variable, formula)
            return formula
        else:
            return Exists(self.variable, self.children[0].expand_quantifiers())

    @typechecked
    def move_quantifiers_inwards(self) -> tc.Formula:
        assert isinstance(self.variable, tc.Variable)

        if not self.children[0].contains_variable(self.variable):
            return self.children[0].move_quantifiers_inwards()

        if isinstance(self.children[0], tc.And):
            if self.children[0].children[0].contains_variable(
                self.variable
            ) and not self.children[0].children[1].contains_variable(self.variable):
                return tc.And(
                    Exists(self.variable, self.children[0].children[0]),
                    self.children[0].children[1],
                ).move_quantifiers_inwards()
            elif self.children[0].children[1].contains_variable(
                self.variable
            ) and not self.children[0].children[0].contains_variable(self.variable):
                return tc.And(
                    self.children[0].children[0],
                    Exists(self.variable, self.children[0].children[1]),
                ).move_quantifiers_inwards()
            else:
                return Exists(
                    self.variable, self.children[0].move_quantifiers_inwards()
                )

        if isinstance(self.children[0], tc.Or):
            if self.children[0].children[0].contains_variable(
                self.variable
            ) and not self.children[0].children[1].contains_variable(self.variable):
                return tc.Or(
                    Exists(self.variable, self.children[0].children[0]),
                    self.children[0].children[1],
                ).move_quantifiers_inwards()
            elif self.children[0].children[1].contains_variable(
                self.variable
            ) and not self.children[0].children[0].contains_variable(self.variable):
                return tc.Or(
                    self.children[0].children[0],
                    Exists(self.variable, self.children[0].children[1]),
                ).move_quantifiers_inwards()
            else:
                return Exists(
                    self.variable, self.children[0].move_quantifiers_inwards()
                )

        if isinstance(self.children[0], tc.Not):
            # prefer exists over forall
            return Exists(self.variable, self.children[0].move_quantifiers_inwards())

        return Exists(self.variable, self.children[0].move_quantifiers_inwards())

    @typechecked
    def _move_same_type_quantifiers_outwards(
        self, move_exists: bool, move_forall: bool
    ) -> tc.Formula:
        return Exists(
            self.variable,
            self.children[0]._move_same_type_quantifiers_outwards(
                move_exists=True, move_forall=False
            ),
        )

    @typechecked
    def _to_sql(self) -> str:
        from_query = ""
        if isinstance(self.variable, set):
            for var in self.variable:
                from_query += f"{var.type} AS {var.name}, "
            from_query = from_query[: -len(", ")]
        else:
            from_query = f"{self.variable.type} AS {self.variable.name}"
        return f"EXISTS (SELECT NULL FROM {from_query} WHERE ({self.children[0]._to_sql()}))"

    @typechecked
    def flatten_quantifiers(self) -> tc.Formula:
        if isinstance(self.children[0], Exists):
            if isinstance(self.variable, set) and isinstance(
                self.children[0].variable, set
            ):
                new_variable = self.variable | self.children[0].variable
            elif isinstance(self.variable, set) and not isinstance(
                self.children[0].variable, set
            ):
                new_variable = self.variable | {self.children[0].variable}
            elif not isinstance(self.variable, set) and isinstance(
                self.children[0].variable, set
            ):
                new_variable = {self.variable} | self.children[0].variable
            else:
                new_variable = {self.variable, self.children[0].variable}
            return Exists(
                new_variable, self.children[0].children[0]
            ).flatten_quantifiers()
        else:
            return Exists(self.variable, self.children[0].flatten_quantifiers())

    @typechecked
    def _to_normal_form(self) -> tc.Formula:
        if isinstance(self.variable, set):
            formula = self.children[0]._to_normal_form()
            for var in self.variable:
                formula = Exists(var, formula)
            return formula
        return Exists(self.variable, self.children[0]._to_normal_form())

    @typechecked
    def contains_variable(self, variable: tc.Variable) -> bool:
        return (
            variable in self.variable
            if isinstance(self.variable, set)
            else self.variable == variable
        ) or self.children[0].contains_variable(variable)

    @typechecked
    def contains_variable_typing(self, variable: tc.Variable) -> bool:
        return (
            variable in self.variable
            if isinstance(self.variable, set)
            else self.variable == variable
        ) or self.children[0].contains_variable_typing(variable)

    @typechecked
    def _rename_variable(
        self, old_variable: tc.Variable, new_variable: tc.Variable
    ) -> tc.Formula:
        if self.variable == old_variable:
            self.variable = new_variable
        if self.children[0] == old_variable:
            Exists(self.variable, new_variable)
        return Exists(
            self.variable, self.children[0]._rename_variable(old_variable, new_variable)
        )

    @typechecked
    def _prune_variable_atoms(self) -> tc.Formula | None:
        new_child = self.children[0]._prune_variable_atoms()
        if new_child is None:
            raise Exception(
                "Invalid input: Eine deklarierte Variable kann nicht quantifiziert werden"
            )

        return Exists(self.variable, new_child)

    @typechecked
    def get_used_variables(self) -> set[tc.Variable]:
        child_vars = self.children[0].get_used_variables()
        if isinstance(self.variable, set):
            return child_vars.union(self.variable)
        return child_vars.union({self.variable})

    @typechecked
    def _check_variable_legality(self, variable: tc.Variable) -> bool:
        if self.variable != variable:
            return self.children[0]._check_variable_legality(variable)

        if self.children[0].contains_variable_typing(variable):
            raise Exception(
                "Invalid input: Eine deklarierte Variable kann nicht quantifiziert werden"
            )

        return True
