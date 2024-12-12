from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.domain_calculus as dc


class Result:
    @typechecked
    def __init__(self, variables: list[dc.Variable]) -> None:
        """
        Parameters
        ----------
        variables : list[Variable]
            The variables that should be returned.
        """
        if len(variables) == 0:
            raise Exception("Mindestens eine Variable in variables benötigt")
        self.variables = variables

    @typechecked
    def __copy__(self) -> Result:
        return deepcopy(self)

    @typechecked
    def __deepcopy__(self, memo) -> Result:
        return Result(deepcopy(self.variables, memo))

    @typechecked
    def __repr__(self) -> str:
        output = ""
        for variable in self.variables:
            output += f"\\text{{{variable.name}}}, "
        output = output[:-2]  # remove last ', '
        return output
