import pytest

from relational_calculus.tuple_calculus import *


def test_alternative_syntax():
    var = Variable("name", "Type")
    assert var["a"] == (var, "a")


def test_alternative_syntax_error_multiple():
    var = Variable("name", "Type")
    with pytest.raises(Exception):
        var["a", "b"]


def test_alternative_syntax_error_type():
    var = Variable("name", "Type")
    with pytest.raises(Exception):
        var[1]


def test_fastest_race_laps(session):
    r = session.execute(
        """SELECT circuits.name, drivers.forename, drivers.surname, lapTimes.milliseconds
        FROM circuits
        JOIN races ON circuits.circuitId = races.circuitId
        JOIN lapTimes ON races.raceId = lapTimes.raceId
        JOIN drivers ON lapTimes.driverId = drivers.driverId
        WHERE NOT EXISTS (
            SELECT *
            FROM lapTimes lT
            WHERE lT.raceId = lapTimes.raceId
            AND (lapTimes.driverID != lT.driverID OR lapTimes.lap != lT.lap)
            AND lapTimes.milliseconds < lT.milliseconds
        );"""
    )
    solution = set(r.fetchall())
    assert len(solution) > 0

    circuit = Variable("circuit", "Circuits")
    race = Variable("race", "Races")
    lapTime = Variable("lapTime", "lapTimes")
    driver = Variable("driver", "Drivers")

    c2 = Variable("c2", "Circuits")
    r2 = Variable("r2", "Races")
    lT2 = Variable("lT2", "lapTimes")
    d2 = Variable("d2", "Drivers")

    tc = TupleCalculus(
        Result(
            [
                circuit["name"],
                driver["forename"],
                driver["surname"],
                lapTime["milliseconds"],
            ]
        ),
        And(
            And(And(circuit, lapTime), driver),
            Exists(
                race,
                And(
                    # Join On
                    And(
                        Equals(circuit["circuitId"], race["circuitId"]),
                        And(
                            Equals(race["raceId"], lapTime["raceId"]),
                            Equals(lapTime["driverId"], driver["driverId"]),
                        ),
                    ),
                    # Fastest Time
                    Forall(
                        lT2,
                        Or(
                            Not(
                                And(
                                    Equals(lT2["raceId"], lapTime["raceId"]),
                                    Not(
                                        And(
                                            Equals(lT2["driverId"], driver["driverId"]),
                                            Equals(lT2["lap"], lapTime["lap"]),
                                        )
                                    ),
                                )
                            ),
                            LessEquals(lT2["milliseconds"], lapTime["milliseconds"]),
                        ),
                    ),
                ),
            ),
        ),
    )
    r = session.execute(tc.to_sql())
    result = set(r.fetchall())

    assert solution == result
