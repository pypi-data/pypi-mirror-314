from __future__ import annotations

from abc import abstractclassmethod
from copy import deepcopy

from docstring_inheritance import NumpyDocstringInheritanceMeta
from typeguard import typechecked

import relational_calculus.tuple_calculus as tc


class Formula(metaclass=NumpyDocstringInheritanceMeta):
    """
    An abstract class used to represent a first order logic formula.
    This class has many different implementations, together forming a recursive data-structure to hold the formula.
    """

    @typechecked
    def __init__(self, children: list[Formula]) -> None:
        """
        Parameters
        ----------
        children : list[Formula]
            Each implementation of formula can hold a list of children that it is composed of.
        """
        self.children = children

    @typechecked
    def __copy__(self) -> Formula:
        """
        Returns a copy of the formula.

        Returns
        -------
        Formula
            A copy of the formula.
        """
        return deepcopy(self)

    @typechecked
    @abstractclassmethod
    def __deepcopy__(self, memo) -> Formula:
        """
        Returns a deep copy of the formula.

        Returns
        -------
        Formula
            A deep copy of the formula.
        """
        pass

    @typechecked
    @abstractclassmethod
    def __repr__(self) -> str:
        """
        Returs a string representation of a given formula formatted in Latex Math Mode.

        Returns
        -------
        str
            A string representation of the formula formatted in Latex Math Mode.
        """
        pass

    @typechecked
    @abstractclassmethod
    def __eq__(self, other) -> bool:
        """
        Check for equality of syntax, not semantics.

        Returns
        -------
        bool
            If the objects are equal.
        """
        pass

    @typechecked
    def verify(self) -> bool:
        """
        Check if the formula is valid.

        Returns
        -------
        bool
            If the formula is valid.
        """
        formula = self.to_normal_form()
        variables = formula.get_used_variables()
        check = True
        for variable in variables:
            check = check and formula.check_variable_legality(variable)
        return check

    @typechecked
    def optimize(self) -> Formula | None:
        """
        Optimize the formula. Also prunes the variable atoms.

        Returns
        -------
        Formula
            The optimized formula.
        """
        # prune variable atoms
        formula = self
        formula = formula.prune_variable_atoms()
        if formula is None:
            return None

        # expand all quantifiers
        formula = formula.expand_quantifiers()

        # move all quantifiers inwards, do not split (at connectives)
        formula = formula.move_quantifiers_inwards()

        # move more inward quantifiers of same type outwards
        formula = formula.move_same_type_quantifiers_outwards()

        # flatten adjecent quantifiers
        formula = formula.flatten_quantifiers()

        return formula

    @typechecked
    def expand_quantifiers(self) -> Formula:
        """
        Expand all quantifiers.

        Returns
        -------
        Formula
            The formula with all quantifiers expanded.
        """
        pass

    @typechecked
    def move_quantifiers_inwards(self) -> Formula:
        """
        Move all quantifiers inwards, do not split (at connectives).
        Use only after expanding all quantifiers (see Formula::expand_quantifiers).

        Returns
        -------
        Formula
            The formula with all quantifiers moved inwards.
        """
        pass

    @typechecked
    def move_same_type_quantifiers_outwards(self) -> Formula:
        """
        Move more inward quantifiers of same type outwards.

        Returns
        -------
        Formula
            The formula with more inward quantifiers of same type moved outwards.
        """
        formula = self
        new_formula = formula._move_same_type_quantifiers_outwards(
            move_exists=True, move_forall=False
        )
        while formula != new_formula:
            formula = new_formula
            new_formula = formula._move_same_type_quantifiers_outwards(
                move_exists=True, move_forall=False
            )
        return formula

    @typechecked
    def _move_same_type_quantifiers_outwards(
        self, move_exists: bool, move_forall: bool
    ) -> Formula:
        """
        Move more inward quantifiers of same type outwards.

        Parameters
        ----------
        move_exists : bool
            If exists quantifiers should be moved outwards.
        move_forall : bool
            If forall quantifiers should be moved outwards.

        Returns
        -------
        Formula
            The formula with more inward quantifiers of same type moved outwards.
        """
        pass

    @typechecked
    def to_sql(self) -> str:
        """
        Used by TupleCalculus::to_sql to convert the tuple calculus specification into an equivalent SQL formula.

        Returns
        -------
        str
            The sub_query in SQL generated by this formula.
        """
        formula = self.prune_variable_atoms()
        if formula is not None:
            formula = formula.flatten_quantifiers()
            return formula._to_sql()
        return ""

    @typechecked
    @abstractclassmethod
    def _to_sql(self) -> str:
        """
        Used by Formula::to_sql to convert the tuple calculus specification into an equivalent SQL formula.
        This method only returns the desired output after the formula has been pruned of Variable-atoms (see Formula::prune_variable_atoms).

        Returns
        -------
        str
            The sub_query in SQL generated by this formula.
        """
        pass

    @typechecked
    def flatten_quantifiers(self) -> Formula:
        """
        Groups adjecent quantifiers of the same type toghether

        Returns
        -------
        Formula
            The flattened formula.
        """
        pass

    @typechecked
    def to_normal_form(self) -> Formula:
        """
        Converts a given formula into an semantically equivalent Formula close to Prenex-Normalform.

        Returns
        -------
        Formula
            The semantically equivalent Formula close to Prenex-Normalform.
        """
        formula = self
        new_formula = formula._to_normal_form()
        while formula != new_formula:
            formula = new_formula
            new_formula = formula._to_normal_form()
        return formula

    @typechecked
    @abstractclassmethod
    def _to_normal_form(self) -> Formula:
        """
        Converts a given formula into an semantically equivalent Formula close to Prenex-Normalform.

        Returns
        -------
        Formula
            The semantically equivalent Formula close to Prenex-Normalform.
        """
        pass

    @typechecked
    @abstractclassmethod
    def contains_variable(self, variable: tc.Variable) -> bool:
        """
        Checks whether a given formula contains a given variable.

        Parameters
        ----------
        variable : Variable
            The variable to check in the formula.
        """
        pass

    @typechecked
    @abstractclassmethod
    def contains_variable_typing(self, variable: tc.Variable) -> bool:
        """
        Checks whether a given formula contains a given variable.

        Parameters
        ----------
        variable : Variable
            The variable to check in the formula.
        """
        pass

    _rename_index = 0

    @typechecked
    def rename_variable(self, variable: tc.Variable) -> Formula:
        """
        Renames a variable to an unused name and replaces all occurences of the old variable with the new one.

        Parameters
        ----------
        variable : Variable
            The variable to rename.
        """
        Formula._rename_index += 1
        new_variable = tc.Variable(
            variable.name + str(Formula._rename_index), variable.type
        )
        return self._rename_variable(variable, new_variable)

    @typechecked
    @abstractclassmethod
    def _rename_variable(
        self, old_variable: tc.Variable, new_variable: tc.Variable
    ) -> Formula:
        """
        Replaces all old occurences of an old variable with the new variable.

        Parameters
        ----------
        old_variable : Variable
            The variable to replace.
        new_variable : Variable
            The variable to replace with.
        """
        pass

    @typechecked
    def prune_variable_atoms(self) -> Formula | None:
        """
        Converts a given formula into a formula stripped of Variable-atoms.

        Returns
        -------
        Formula
            The formula stripped of Variable-atoms.
        """
        formula = self
        new_formula = formula._prune_variable_atoms()
        while formula != new_formula and new_formula is not None:
            formula = new_formula
            new_formula = formula._prune_variable_atoms()
        return new_formula

    @typechecked
    @abstractclassmethod
    def _prune_variable_atoms(self) -> Formula | None:
        """
        Converts a given formula into a formula stripped of Variable-atoms.

        Returns
        -------
        Formula
            The formula stripped of Variable-atoms.
        """
        pass

    @typechecked
    @abstractclassmethod
    def get_used_variables(self) -> set[tc.Variable]:
        """
        Returns a set of variables used in a given formula.

        Returns
        -------
        set[Variable]
            A set of variables used in the formula.
        """
        pass

    @typechecked
    def check_variable_legality(self, variable: tc.Variable) -> bool:
        """
        Checks if a given variable is used correctly in the given formula.

        Parameters
        ----------
        variable : Variable
            The variable to check the legal use of.

        Returns
        -------
        true
            If the variable's usage was legal.
        false
            Otherwise.

        Raises
        ------
        Exception
            If the variable was not used legally. The exception message also holds further explanation.
        """
        return self.contains_variable_typing(
            variable
        ) and self.to_normal_form()._check_variable_legality(variable)

    @typechecked
    @abstractclassmethod
    def _check_variable_legality(self, variable: tc.Variable) -> bool:
        """
        Checks if a given variable is used correctly in the given formula.

        Parameters
        ----------
        variable : Variable
            The variable to check the legal use of.

        Returns
        -------
        true
            If the variable's usage was legal.
        false
            Otherwise.

        Raises
        ------
        Exception
            If the variable was not used legally. The exception message also holds further explanation.
        """
        pass
