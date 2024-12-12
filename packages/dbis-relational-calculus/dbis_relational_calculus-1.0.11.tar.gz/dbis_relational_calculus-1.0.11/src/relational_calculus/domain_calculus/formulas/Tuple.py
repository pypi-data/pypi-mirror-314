from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

from typing import Any, Optional

import relational_calculus.domain_calculus as dc


class Tuple(dc.Formula):
    new_var_index = 1  # for the conversion of Non-Variables in Tuples to Variables

    @typechecked
    def __init__(
        self, type: str, variables: list[dc.Variable | dc.PRIMITIVE_TYPES | None]
    ) -> None:
        super().__init__([])
        if len([value for value in variables if value is not None]) == 0:
            raise Exception("Das Tupel braucht mindestens eine Variable")
        self.type = type.upper()
        self.variables = variables

    @typechecked
    def __deepcopy__(self, memo) -> Tuple:
        return Tuple(self.type, deepcopy(self.variables, memo))

    @typechecked
    def __repr__(self) -> str:
        output = f"\\text{{{self.type}}}("
        for variable in self.variables:
            if isinstance(variable, dc.Variable):
                output += f"\\text{{{variable.name}}}, "
            elif isinstance(variable, dc.PRIMITIVE_TYPES):
                output += f'\\text{{"{variable}"}}, '
            elif variable is None:
                output += f"\\_\\_, "

        output = output[: -len(", ")]  # remove last ', '
        output += ")"
        return output

    @typechecked
    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Tuple)
            and self.type == other.type
            and self.variables == other.variables
        )

    @typechecked
    def __hash__(self) -> int:
        return hash(
            tuple(
                (
                    Tuple,
                    self.type,
                    ", ".join(list(map(lambda var: str(var.name), self.variables))),
                )
            )
        )

    @typechecked
    def _to_sql(self) -> Optional[str]:
        # will be handled in DomainCalculus.to_sql()
        return ""

    @typechecked
    def _to_normal_form(self) -> dc.Formula:
        new_variables = dict()
        new_tuple = list()
        new_vars = list()
        for var in self.variables:
            if isinstance(var, dc.Variable):
                new_tuple.append(var)
            elif isinstance(var, dc.PRIMITIVE_TYPES):
                new_var = dc.Variable(f"{self.type}_{var}_{Tuple.new_var_index}")
                new_variables[new_var] = var
                new_tuple.append(new_var)
                new_vars.append(new_var)
                Tuple.new_var_index += 1
            elif var is None:
                new_var = dc.Variable(f"{self.type}_placeholder_{Tuple.new_var_index}")
                new_tuple.append(new_var)
                new_vars.append(new_var)
                Tuple.new_var_index += 1
        formula = Tuple(self.type, new_tuple)
        for new_var in new_vars:
            if new_var in new_variables.keys():
                formula = dc.Exists(
                    new_var, dc.And(formula, dc.Equals(new_var, new_variables[new_var]))
                )
            else:
                formula = dc.Exists(new_var, formula)
        return formula

    @typechecked
    def contains_variable(self, variable: dc.Variable) -> bool:
        return variable in self.variables

    @typechecked
    def contains_variable_typing(self, variable: dc.Variable) -> bool:
        return self.contains_variable(variable)

    @typechecked
    def contains_variable_quantification(self, variable: dc.Variable) -> bool:
        return False

    @typechecked
    def _rename_variable(
        self, old_variable: dc.Variable, new_variable: dc.Variable
    ) -> dc.Formula:
        new_tuple = list()
        for var in self.variables:
            if isinstance(var, dc.Variable):
                if var == old_variable:
                    new_tuple.append(new_variable)
                else:
                    new_tuple.append(var)
            elif isinstance(var, dc.PRIMITIVE_TYPES):
                new_tuple.append(var)
            elif var is None:
                new_tuple.append(None)
        return Tuple(self.type, new_tuple)

    @typechecked
    def _prune_tuple_atoms(self) -> dc.Formula | None:
        return None

    @typechecked
    def get_used_variables(self) -> set[dc.Variable]:
        return set(var for var in self.variables if isinstance(var, dc.Variable))

    @typechecked
    def get_used_tuples(self) -> set[dc.Tuple]:
        return {self}

    @typechecked
    def _check_variable_legality(self, variable: dc.Variable) -> bool:
        return True
