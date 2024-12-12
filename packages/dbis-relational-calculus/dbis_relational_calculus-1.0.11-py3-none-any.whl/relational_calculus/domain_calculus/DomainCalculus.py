from __future__ import annotations

from copy import deepcopy

from typeguard import typechecked

import relational_calculus.domain_calculus as dc
from relational_calculus.domain_calculus.formulas.quantifiers.Forall import Forall


class DomainCalculus:
    @typechecked
    def __init__(self, result: dc.Result, formula: dc.Formula) -> None:
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
    def __copy__(self) -> DomainCalculus:
        return deepcopy(self)

    @typechecked
    def __deepcopy__(self, memo) -> DomainCalculus:
        return DomainCalculus(deepcopy(self.result, memo), deepcopy(self.formula, memo))

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
        variables = self.result.variables

        for variable in variables:
            check = check and self.formula.check_variable_legality(variable)

        return check

    @typechecked
    def __repr__(self) -> str:
        return f"\\{{[{self.result}] \\ \\vert \\ {self.formula}\\}}"

    @typechecked
    def to_sql(self) -> str:
        """
        Convert the domain calculus to a SQL query.

        Returns
        -------
        str
            The SQL query.
        """
        return deepcopy(self).__to_sql()

    @typechecked
    def __to_sql(self) -> str:
        """
        Convert the domain calculus to a SQL query.

        Returns
        -------
        str
            The SQL query.
        """
        # Select Statement
        select_query = "SELECT DISTINCT "
        for variable in self.result.variables:
            select_query += f'"{variable.name}", '
        select_query = select_query[: -len(", ")]  # remove last ', '

        formula = self.formula.to_normal_form()
        used_tuples = formula.get_used_tuples()

        # Map Tuples to new Table Names
        id = 1
        tuple_mapping = dict()
        for tuple in used_tuples:
            tuple_mapping[tuple] = f"table_{id}"
            id += 1

        # Determine Tuples containing return variables
        result_tuples = set()
        for variable in self.result.variables:
            for tuple in used_tuples:
                if variable in tuple.variables:
                    result_tuples.add(tuple)

        # Determine other tuples order and type
        tuple_quantification = dict()
        tuple_order = list()
        while isinstance(formula, dc.QUANTIFIER_TYPES):
            variables = set()
            if isinstance(formula.variable, set):
                variables = formula.variable
            else:
                variables.add(formula.variable)
            for variable in variables:
                for tuple in used_tuples:
                    if tuple in result_tuples:
                        continue
                    if variable in tuple.variables:
                        if tuple not in tuple_order:
                            tuple_order.append(tuple)
                            tuple_quantification[tuple] = isinstance(formula, Forall)
                        else:
                            assert tuple in tuple_quantification.keys()
                            tuple_quantification[tuple] = (
                                isinstance(formula, Forall)
                                or tuple_quantification[tuple]
                            )
            formula = formula.children[0]

        # Create regions of adjecent tuples of the same type (Exists, Forall)
        tuple_regions = list()
        current_region = list()
        for tuple in tuple_order:
            if len(current_region) == 0:
                current_region.append(tuple)
            elif tuple_quantification[tuple] == tuple_quantification[current_region[0]]:
                current_region.append(tuple)
            else:
                tuple_regions.append(current_region)
                current_region = list()
                current_region.append(tuple)
        if len(current_region) > 0:
            tuple_regions.append(current_region)

        # With-As Statements
        with_query = "WITH "
        for tuple in used_tuples:
            __quotation_mark = '"'  # cannot use backslash in f''-string
            with_query += f'{tuple_mapping[tuple]}({",".join(list(map(lambda var: __quotation_mark + var.name + __quotation_mark, tuple.variables)))}) AS (SELECT * FROM {tuple.type}), '
        with_query = with_query[: -len(", ")]

        # From Statement
        from_query = " FROM "
        for tuple in result_tuples:
            from_query += f"{tuple_mapping[tuple]} NATURAL JOIN "
        from_query = from_query[: -len(" NATURAL JOIN ")]

        # Where Statement
        where_sub_query = formula.to_sql()
        where_query = ""
        if where_sub_query is not None and where_sub_query != "":
            where_query = " WHERE "
            bracket_counter = 0
            previous_tuples = list(result_tuples)
            if len(tuple_regions) > 0:
                for region in tuple_regions:
                    _from_sub_query = "FROM "
                    for tuple in region:
                        _from_sub_query += f"{tuple_mapping[tuple]} NATURAL JOIN "
                    _from_sub_query = _from_sub_query[: -len(" NATURAL JOIN ")]

                    _where_sub_query = "WHERE"
                    for previous_tuple in previous_tuples:
                        for tuple in region:
                            for variable in previous_tuple.variables:
                                if variable in tuple.variables:
                                    _where_sub_query += f" {tuple_mapping[previous_tuple]}.{variable.name} = {tuple_mapping[tuple]}.{variable.name} AND"

                    if tuple_quantification[region[0]]:
                        where_query += f"NOT EXISTS (SELECT NULL {_from_sub_query} {_where_sub_query} NOT ("
                        bracket_counter += 2
                    else:
                        where_query += (
                            f"EXISTS (SELECT NULL {_from_sub_query} {_where_sub_query} "
                        )
                        bracket_counter += 1
                    previous_tuples.extend(region)

            where_query += where_sub_query
            where_query += ")" * bracket_counter

        return f"{with_query} {select_query} {from_query} {where_query}"
