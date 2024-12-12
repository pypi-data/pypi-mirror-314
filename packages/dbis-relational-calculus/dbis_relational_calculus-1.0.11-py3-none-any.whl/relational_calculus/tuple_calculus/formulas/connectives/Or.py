from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class Or(tc.Formula):
    """
    A class representing the logical connective 'or'.
    """

    @typechecked
    def __init__(self, left: tc.Formula, right: tc.Formula) -> None:
        """
        Parameters
        ----------
        left : Formula
            Left subformula.
        right : Formula
            Right subformula.
        """
        super().__init__([left, right])

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
            if not isinstance(left_grandchild, Or | tc.ATOM_TYPES | tc.Variable):
                left_repr = f"({left_repr})"
            if not isinstance(right_grandchild, Or | tc.ATOM_TYPES | tc.Variable):
                right_repr = f"({right_repr})"
            left = f"{left_repr} \\lor {right_repr}"
        elif not isinstance(self.children[0], tc.Not | tc.ATOM_TYPES | tc.Variable):
            left = f"({left})"

        if isinstance(self.children[1], Or):
            left_grandchild = self.children[1].children[0]
            right_grandchild = self.children[1].children[1]
            left_repr = f"{left_grandchild}"
            right_repr = f"{right_grandchild}"
            if not isinstance(left_grandchild, Or | tc.ATOM_TYPES | tc.Variable):
                left_repr = f"({left_repr})"
            if not isinstance(right_grandchild, Or | tc.ATOM_TYPES | tc.Variable):
                right_repr = f"({right_repr})"
            right = f"{left_repr} \\lor {right_repr}"
        elif not isinstance(self.children[1], tc.Not | tc.ATOM_TYPES | tc.Variable):
            right = f"({right})"

        return f"{left} \\lor {right}"

    @typechecked
    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Or)
            and self.children[0] == other.children[0]
            and self.children[1] == other.children[1]
        )

    @typechecked
    def expand_quantifiers(self) -> tc.Formula:
        return Or(
            self.children[0].expand_quantifiers(), self.children[1].expand_quantifiers()
        )

    @typechecked
    def move_quantifiers_inwards(self) -> tc.Formula:
        return Or(
            self.children[0].move_quantifiers_inwards(),
            self.children[1].move_quantifiers_inwards(),
        )

    @typechecked
    def _move_same_type_quantifiers_outwards(
        self, move_exists: bool, move_forall: bool
    ) -> tc.Formula:
        if move_exists:
            if isinstance(self.children[0], tc.Exists):
                variable = self.children[0].variable
                if self.children[1].contains_variable(variable):
                    return Or(
                        self.children[0].rename_variable(variable), self.children[1]
                    )._move_same_type_quantifiers_outwards(
                        move_exists=True, move_forall=False
                    )
                else:
                    return tc.Exists(
                        variable,
                        Or(
                            self.children[0].children[0], self.children[1]
                        )._move_same_type_quantifiers_outwards(
                            move_exists=True, move_forall=False
                        ),
                    )
            if isinstance(self.children[1], tc.Exists):
                variable = self.children[1].variable
                if self.children[0].contains_variable(variable):
                    return Or(
                        self.children[0], self.children[1].rename_variable(variable)
                    )._move_same_type_quantifiers_outwards(
                        move_exists=True, move_forall=False
                    )
                else:
                    return tc.Exists(
                        variable,
                        Or(
                            self.children[0], self.children[1].children[0]
                        )._move_same_type_quantifiers_outwards(
                            move_exists=True, move_forall=False
                        ),
                    )

        if move_forall:
            if isinstance(self.children[0], tc.Forall):
                variable = self.children[0].variable
                if self.children[1].contains_variable(variable):
                    return Or(
                        self.children[0].rename_variable(variable), self.children[1]
                    )._move_same_type_quantifiers_outwards(
                        move_exists=False, move_forall=True
                    )
                else:
                    return tc.Forall(
                        variable,
                        Or(
                            self.children[0].children[0], self.children[1]
                        )._move_same_type_quantifiers_outwards(
                            move_exists=False, move_forall=True
                        ),
                    )
            if isinstance(self.children[1], tc.Forall):
                variable = self.children[1].variable
                if self.children[0].contains_variable(variable):
                    return Or(
                        self.children[0], self.children[1].rename_variable(variable)
                    )._move_same_type_quantifiers_outwards(
                        move_exists=False, move_forall=True
                    )
                else:
                    return tc.Forall(
                        variable,
                        Or(
                            self.children[0], self.children[1].children[0]
                        )._move_same_type_quantifiers_outwards(
                            move_exists=False, move_forall=True
                        ),
                    )

        return Or(
            self.children[0]._move_same_type_quantifiers_outwards(
                move_exists=move_exists, move_forall=move_forall
            ),
            self.children[1]._move_same_type_quantifiers_outwards(
                move_exists=move_exists, move_forall=move_forall
            ),
        )

    @typechecked
    def _to_sql(self) -> str:
        left = self.children[0]._to_sql()
        right = self.children[1]._to_sql()

        if left == "" and right == "":
            return ""
        if left == "" and right != "":
            return right
        if left != "" and right == "":
            return left

        left = f"({left})"
        right = f"({right})"

        return f"{left} OR {right}"

    @typechecked
    def flatten_quantifiers(self) -> tc.Formula:
        return Or(
            self.children[0].flatten_quantifiers(),
            self.children[1].flatten_quantifiers(),
        )

    @typechecked
    def _to_normal_form(self) -> tc.Formula:
        if isinstance(self.children[0], tc.Exists):
            self.children[0] = self.children[0]._to_normal_form()
            variable = self.children[0].variable
            if self.children[1].contains_variable(variable):
                return Or(
                    self.children[0].rename_variable(variable), self.children[1]
                )._to_normal_form()
            else:
                return tc.Exists(
                    variable,
                    Or(
                        self.children[0].children[0], self.children[1]
                    )._to_normal_form(),
                )

        if isinstance(self.children[0], tc.Forall):
            self.children[0] = self.children[0]._to_normal_form()
            variable = self.children[0].variable
            if self.children[1].contains_variable(variable):
                return Or(
                    self.children[0].rename_variable(variable), self.children[1]
                )._to_normal_form()
            else:
                return tc.Forall(
                    variable,
                    Or(
                        self.children[0].children[0], self.children[1]
                    )._to_normal_form(),
                )

        if isinstance(self.children[1], tc.Exists):
            self.children[1] = self.children[1]._to_normal_form()
            variable = self.children[1].variable
            if self.children[0].contains_variable(variable):
                return Or(
                    self.children[0], self.children[1].rename_variable(variable)
                )._to_normal_form()
            else:
                return tc.Exists(
                    variable,
                    Or(
                        self.children[0], self.children[1].children[0]
                    )._to_normal_form(),
                )

        if isinstance(self.children[1], tc.Forall):
            self.children[1] = self.children[1]._to_normal_form()
            variable = self.children[1].variable
            if self.children[0].contains_variable(variable):
                return Or(
                    self.children[0], self.children[1].rename_variable(variable)
                )._to_normal_form()
            else:
                return tc.Forall(
                    variable,
                    Or(
                        self.children[0], self.children[1].children[0]
                    )._to_normal_form(),
                )

        return Or(
            self.children[0]._to_normal_form(), self.children[1]._to_normal_form()
        )

    @typechecked
    def contains_variable(self, variable: tc.Variable) -> bool:
        return self.children[0].contains_variable(variable) or self.children[
            1
        ].contains_variable(variable)

    @typechecked
    def contains_variable_typing(self, variable: tc.Variable) -> bool:
        return self.children[0].contains_variable_typing(variable) or self.children[
            1
        ].contains_variable_typing(variable)

    @typechecked
    def _rename_variable(
        self, old_variable: tc.Variable, new_variable: tc.Variable
    ) -> tc.Formula:
        if self.children[0] == old_variable and self.children[1] == old_variable:
            return Or(new_variable, new_variable)

        if self.children[0] != old_variable and self.children[1] == old_variable:
            return Or(
                self.children[0]._rename_variable(old_variable, new_variable),
                new_variable,
            )

        if self.children[0] == old_variable and self.children[1] != old_variable:
            return Or(
                new_variable,
                self.children[1]._rename_variable(old_variable, new_variable),
            )

        return Or(
            self.children[0]._rename_variable(old_variable, new_variable),
            self.children[1]._rename_variable(old_variable, new_variable),
        )

    @typechecked
    def _prune_variable_atoms(self) -> tc.Formula | None:
        new_left = self.children[0]._prune_variable_atoms()
        new_right = self.children[1]._prune_variable_atoms()

        if new_left is None:
            return new_right

        if new_right is None:
            return new_left

        return Or(new_left, new_right)

    @typechecked
    def get_used_variables(self) -> set[tc.Variable]:
        return (
            self.children[0]
            .get_used_variables()
            .union(self.children[1].get_used_variables())
        )

    @typechecked
    def _check_variable_legality(self, variable: tc.Variable) -> bool:
        if self.children[0].contains_variable_typing(variable) and self.children[
            1
        ].contains_variable_typing(variable):
            # cannot happen due to renaming of variables
            raise Exception("Internal Error")

        if self.children[0].contains_variable_typing(variable) and self.children[
            1
        ].contains_variable(variable):
            raise Exception("Jede Variable muss vor der Nutzung deklariert sein")

        if self.children[0].contains_variable(variable) and self.children[
            1
        ].contains_variable_typing(variable):
            raise Exception("Jede Variable muss vor der Nutzung deklariert sein")

        return self.children[0]._check_variable_legality(variable) and self.children[
            1
        ]._check_variable_legality(variable)
