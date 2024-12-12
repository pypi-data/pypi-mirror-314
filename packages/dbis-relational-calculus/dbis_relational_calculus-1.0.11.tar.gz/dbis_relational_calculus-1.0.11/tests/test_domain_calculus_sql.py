import pytest

from relational_calculus.domain_calculus import *


def test_track_refs(session):
    r = session.execute("SELECT circuitRef FROM circuits;")
    solution = set(r.fetchall())
    assert len(solution) > 0

    cR = Variable("circuitRef")
    dc = DomainCalculus(
        Result([cR]), Tuple("circuits", [None, cR, None, None, None, None, None])
    )
    r = session.execute(dc.to_sql())
    result = set(r.fetchall())

    assert solution == result


def test_tracks_germany(session):
    r = session.execute(
        "SELECT Name, Location FROM circuits WHERE Country = 'Germany';"
    )
    solution = set(r.fetchall())
    assert len(solution) > 0

    name = Variable("name")
    location = Variable("location")
    dc = DomainCalculus(
        Result([name, location]),
        Tuple("circuits", [None, None, name, location, "Germany", None, None]),
    )
    r = session.execute(dc.to_sql())
    result = set(r.fetchall())

    assert solution == result


def test_tracks_northeast_southwest(session):
    r = session.execute(
        "SELECT * FROM circuits WHERE (Lat >= 0 AND Lng >= 0) OR (Lat < 0 AND Lng < 0);"
    )
    solution = set(r.fetchall())
    assert len(solution) > 0

    circuitId = Variable("id")
    circuitRef = Variable("red")
    name = Variable("ref")
    location = Variable("loc")
    country = Variable("country")
    lat = Variable("lat")
    lng = Variable("lng")
    dc = DomainCalculus(
        Result([circuitId, circuitRef, name, location, country, lat, lng]),
        And(
            Tuple(
                "circuits", [circuitId, circuitRef, name, location, country, lat, lng]
            ),
            Or(
                And(GreaterEquals(lat, 0), GreaterEquals(lng, 0)),
                And(LessThan(lat, 0), LessThan(lng, 0)),
            ),
        ),
    )
    r = session.execute(dc.to_sql())
    result = set(r.fetchall())

    assert solution == result


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

    cN = Variable("cN")
    dF = Variable("dF")
    dS = Variable("dS")
    lM = Variable("lM")
    lL = Variable("lL")

    cI = Variable("cI")
    dI = Variable("dI")
    rI = Variable("rI")

    dI2 = Variable("dI2")
    lM2 = Variable("lM2")
    lL2 = Variable("lL2")
    dc = DomainCalculus(
        Result([cN, dF, dS, lM]),
        Exists(
            {cI, dI, rI},
            And(
                Tuple("races", [rI, None, None, cI, None, None, None]),
                And(
                    Tuple("circuits", [cI, None, cN, None, None, None, None]),
                    And(
                        Tuple("drivers", [dI, None, None, None, dF, dS, None, None]),
                        And(
                            Tuple("lapTimes", [rI, dI, lL, None, None, lM]),
                            Not(
                                Exists(
                                    {dI2, lM2, lL2},
                                    And(
                                        Tuple(
                                            "lapTimes", [rI, dI2, lL2, None, None, lM2]
                                        ),
                                        And(
                                            Or(
                                                Not(Equals(dI, dI2)),
                                                Not(Equals(lL, lL2)),
                                            ),
                                            LessThan(lM, lM2),
                                        ),
                                    ),
                                )
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    r = session.execute(dc.to_sql())
    result = set(r.fetchall())

    assert solution == result
