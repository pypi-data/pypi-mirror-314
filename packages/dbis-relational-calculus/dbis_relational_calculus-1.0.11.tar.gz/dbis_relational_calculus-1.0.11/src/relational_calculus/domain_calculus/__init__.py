from relational_calculus.domain_calculus.Variable import Variable

from relational_calculus.domain_calculus.formulas.Formula import Formula
from relational_calculus.domain_calculus.formulas.Tuple import Tuple

from relational_calculus.domain_calculus.formulas.atoms.Equals import Equals
from relational_calculus.domain_calculus.formulas.atoms.GreaterEquals import (
    GreaterEquals,
)
from relational_calculus.domain_calculus.formulas.atoms.GreaterThan import GreaterThan
from relational_calculus.domain_calculus.formulas.atoms.LessEquals import LessEquals
from relational_calculus.domain_calculus.formulas.atoms.LessThan import LessThan

from relational_calculus.domain_calculus.formulas.connectives.And import And
from relational_calculus.domain_calculus.formulas.connectives.Or import Or
from relational_calculus.domain_calculus.formulas.connectives.Not import Not

from relational_calculus.domain_calculus.formulas.quantifiers.Exists import Exists
from relational_calculus.domain_calculus.formulas.quantifiers.Forall import Forall

from relational_calculus.domain_calculus.Result import Result
from relational_calculus.domain_calculus.DomainCalculus import DomainCalculus

PRIMITIVE_TYPES = int | float | str
ATOM_TYPES = Equals | GreaterEquals | GreaterThan | LessEquals | LessThan
CONNECTIVE_TYPES = And | Or | Not
QUANTIFIER_TYPES = Exists | Forall
