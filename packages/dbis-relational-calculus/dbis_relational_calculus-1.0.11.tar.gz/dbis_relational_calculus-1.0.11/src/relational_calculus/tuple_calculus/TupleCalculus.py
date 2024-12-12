from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class TupleCalculus:
    @typechecked
    def __init__(self, result: tc.Result, formula: tc.Formula) -> None:
        """
        Parameters
        ----------
        result : Result
            The result that should be returned.
        formula : Formula
            The formula that every result has to satisfy.
        """
        self.result = result
        self.formula = formula

    @typechecked
    def __copy__(self) -> TupleCalculus:
        return deepcopy(self)

    @typechecked
    def __deepcopy__(self, memo) -> TupleCalculus:
        return TupleCalculus(deepcopy(self.result, memo), deepcopy(self.formula, memo))

    @typechecked
    def verify(self) -> bool:
        """
        Verify the correctness of the result/formula combination (e.g. one must specify the type of a variable before returning it).

        Returns
        -------
        bool
            True if the result/formula combination is correct, False otherwise.
        """
        assert self.formula is not None
        assert self.result is not None

        check = self.formula.verify()

        # Get Types of return variables
        variables = set()
        for x in self.result.attributes:
            if isinstance(x, tc.Variable):
                variables.add(x)
            elif isinstance(x, tuple):
                variable, _ = x
                variables.add(variable)

        for variable in variables:
            check = check and self.formula.check_variable_legality(variable)

        return check

    @typechecked
    def __repr__(self) -> str:
        return f"\\{{{self.result} \\ \\vert \\ {self.formula}\\}}"

    @typechecked
    def to_sql(self, optimize: bool = True) -> str:
        """
        Convert the domain calculus to a SQL query.

        Parameters
        ----------
        optimize : bool, optional
            If the query should be optimized, by default True

        Returns
        -------
        str
            The SQL query.
        """
        return deepcopy(self).__to_sql(optimize)

    @typechecked
    def __to_sql(self, optimize: bool) -> str:
        """
        Convert the domain calculus to a SQL query.

        Parameters
        ----------
        optimize : bool
            If the query should be optimized

        Returns
        -------
        str
            The SQL query.
        """
        # Get Types of return variables
        variables = set()
        for x in self.result.attributes:
            if isinstance(x, tc.Variable):
                variables.add(x)
            elif isinstance(x, tuple):
                variable, _ = x
                variables.add(variable)

        select_query = ""
        for x in self.result.attributes:
            if isinstance(x, tc.Variable):
                select_query += f"{x.name}.*, "
            elif isinstance(x, tuple):
                variable, attribute = x
                select_query += f"{variable.name}.{attribute}, "

        select_query = select_query[: -len(", ")]

        from_variables = variables
        formula = self.formula
        if optimize:
            formula = formula.optimize()
            if formula is not None:
                if isinstance(formula, tc.Exists):
                    if isinstance(formula.variable, set):
                        from_variables = from_variables.union(formula.variable)
                    else:
                        from_variables.add(formula.variable)
                    formula = formula.children[0]

        from_query = ""
        for variable in from_variables:
            from_query += f"{variable.type} {variable.name}, "
        from_query = from_query[: -len(", ")]

        query = f"SELECT DISTINCT {select_query} FROM {from_query}"

        where_query = None
        if formula is not None:
            where_query = formula.to_sql()

        if where_query is not None and where_query != "":
            query += f" WHERE {where_query}"
        return query
