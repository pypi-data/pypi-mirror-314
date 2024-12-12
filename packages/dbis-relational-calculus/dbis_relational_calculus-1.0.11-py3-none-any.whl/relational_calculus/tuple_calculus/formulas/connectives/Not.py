from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class Not(tc.Formula):
    """
    A class representing the logical negation 'not'.
    """

    @typechecked
    def __init__(self, child: tc.Formula) -> None:
        """
        Parameters
        ----------
        child : Formula
            Subformula.
        """
        super().__init__([child])

    @typechecked
    def __deepcopy__(self, memo) -> Not:
        return Not(deepcopy(self.children[0], memo))

    @typechecked
    def __repr__(self) -> str:
        if isinstance(
            self.children[0],
            tc.And
            | tc.Or
            | tc.Equals
            | tc.GreaterEquals
            | tc.LessEquals
            | tc.GreaterThan
            | tc.LessThan,
        ):
            return f"\\neg({self.children[0]})"
        return f"\\neg {self.children[0]}"

    @typechecked
    def __eq__(self, other) -> bool:
        return isinstance(other, Not) and self.children[0] == other.children[0]

    @typechecked
    def expand_quantifiers(self) -> tc.Formula:
        return Not(self.children[0].expand_quantifiers())

    @typechecked
    def move_quantifiers_inwards(self) -> tc.Formula:
        return Not(self.children[0].move_quantifiers_inwards())

    @typechecked
    def _move_same_type_quantifiers_outwards(
        self, move_exists: bool, move_forall: bool
    ) -> tc.Formula:
        if move_exists:
            # prefer exists over forall
            if isinstance(self.children[0], tc.Forall):
                return tc.Exists(
                    self.children[0].variable, Not(self.children[0].children[0])
                )._move_same_type_quantifiers_outwards(
                    move_exists=True, move_forall=False
                )
            else:
                return Not(
                    self.children[0]._move_same_type_quantifiers_outwards(
                        move_exists=False, move_forall=move_forall
                    )
                )
        else:
            return Not(
                self.children[0]._move_same_type_quantifiers_outwards(
                    move_exists=False, move_forall=False
                )
            )

    @typechecked
    def _to_sql(self) -> str:
        return f"NOT ({self.children[0]._to_sql()})"

    @typechecked
    def flatten_quantifiers(self) -> tc.Formula:
        return Not(self.children[0].flatten_quantifiers())

    @typechecked
    def _to_normal_form(self) -> tc.Formula:
        if isinstance(self.children[0], Not):
            return self.children[0].children[0]._to_normal_form()

        if isinstance(self.children[0], tc.And):
            return tc.Or(
                Not(self.children[0].children[0]), Not(self.children[0].children[0])
            )._to_normal_form()

        if isinstance(self.children[0], tc.Or):
            return tc.And(
                Not(self.children[0].children[0]), Not(self.children[0].children[0])
            )._to_normal_form()

        if isinstance(self.children[0], tc.Exists):
            return tc.Forall(
                self.children[0].variable, Not(self.children[0].children[0])
            )._to_normal_form()

        if isinstance(self.children[0], tc.Forall):
            return tc.Exists(
                self.children[0].variable, Not(self.children[0].children[0])
            )._to_normal_form()

        return Not(self.children[0]._to_normal_form())

    @typechecked
    def contains_variable(self, variable: tc.Variable) -> bool:
        return self.children[0].contains_variable(variable)

    @typechecked
    def contains_variable_typing(self, variable: tc.Variable) -> bool:
        return self.children[0].contains_variable_typing(variable)

    @typechecked
    def _rename_variable(
        self, old_variable: tc.Variable, new_variable: tc.Variable
    ) -> tc.Formula:
        if self.children[0] == old_variable:
            return Not(new_variable)
        return Not(self.children[0]._rename_variable(old_variable, new_variable))

    @typechecked
    def _prune_variable_atoms(self) -> tc.Formula | None:
        new_child = self.children[0]._prune_variable_atoms()
        if new_child is None:
            return None

        return Not(new_child)

    @typechecked
    def get_used_variables(self) -> set[tc.Variable]:
        return self.children[0].get_used_variables()

    @typechecked
    def _check_variable_legality(self, variable: tc.Variable) -> bool:
        if self.children[0].contains_variable_typing(variable):
            # reminder: we are in Normal Form
            raise Exception("Eine Variablendeklaration kann nicht negiert werden")

        return self.children[0]._check_variable_legality(variable)
