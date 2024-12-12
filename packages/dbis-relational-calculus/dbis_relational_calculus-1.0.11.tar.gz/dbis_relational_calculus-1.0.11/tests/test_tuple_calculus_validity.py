import pytest

from relational_calculus.tuple_calculus import *


def test_result_no_variables():
    with pytest.raises(Exception):
        result = Result([])


def test_double_typing_1():
    var = Variable("name", "Type")
    with pytest.raises(Exception):
        Exists(var, var).verify()


def test_double_typing_2():
    var = Variable("name", "Type")
    with pytest.raises(Exception):
        Exists(var, Forall(var, Equals(1, 1)), Equals(1, 1)).verify()


def test_renaming():
    var = Variable("name", "Type")
    formula = Or(Exists(var, Equals(1, 1)), Forall(var, Equals(1, 1)))
    assert len(formula.get_used_variables()) == 1
    formula = formula.to_normal_form()
    assert len(formula.get_used_variables()) == 2
