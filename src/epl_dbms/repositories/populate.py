"""Populate Tables — insert the expanded EPL seed dataset."""

from __future__ import annotations

import oracledb

from epl_dbms.data.seed import (
    ACCOLADES,
    CLUBS,
    FIXTURES,
    MANAGERS,
    PLAYER_STATS,
    PLAYERS,
    STADIUMS,
)


def populate_tables(connection: oracledb.Connection) -> list[str]:
    """
    Insert seed rows in FK-safe order.

    Returns status messages. Existing primary keys are skipped (ORA-00001)
    so re-running Populate is safe without Drop Tables.
    """
    messages: list[str] = []
    cursor = connection.cursor()
    inserted = 0
    skipped = 0

    def _exec(sql: str, params: tuple | dict) -> None:
        nonlocal inserted, skipped
        try:
            cursor.execute(sql, params)
            inserted += 1
        except oracledb.Error as error:
            error_obj, = error.args
            # ORA-00001: unique constraint violated
            if getattr(error_obj, "code", None) == 1:
                skipped += 1
            else:
                raise

    try:
        for stadium_name, capacity in STADIUMS:
            _exec(
                "INSERT INTO Stadiums (Stadium_Name, Stadium_Capacity) VALUES (:1, :2)",
                (stadium_name, capacity),
            )

        for row in CLUBS:
            _exec(
                """
                INSERT INTO Clubs (
                    Team_ID, Club_Name, Valuation, Stadium_Name,
                    Year_Founded, Crest, City
                ) VALUES (:1, :2, :3, :4, :5, :6, :7)
                """,
                row,
            )

        for row in MANAGERS:
            (
                manager_id,
                name,
                team_id,
                joined,
                expiry,
                trophies,
                salary,
                dob,
                formation,
            ) = row
            _exec(
                """
                INSERT INTO Managers (
                    Manager_ID, Manager_Name, Team_ID, Date_Joining,
                    Contract_Expiry_Date, Trophies, Salary, DOB,
                    Preferred_Formation
                ) VALUES (
                    :1, :2, :3,
                    TO_DATE(:4, 'DD-MM-YYYY'),
                    TO_DATE(:5, 'DD-MM-YYYY'),
                    :6, :7,
                    TO_DATE(:8, 'DD-MM-YYYY'),
                    :9
                )
                """,
                (
                    manager_id,
                    name,
                    team_id,
                    joined,
                    expiry,
                    trophies,
                    salary,
                    dob,
                    formation,
                ),
            )

        for row in PLAYERS:
            (
                player_id,
                team_id,
                name,
                crest,
                foot,
                nationality,
                dob,
                position,
                overall,
                height,
                weight,
                attr_kind,
                a1,
                a2,
                a3,
                a4,
                a5,
                a6,
            ) = row
            _exec(
                """
                INSERT INTO Players (
                    Player_ID, Team_ID, Player_Name, Crest, Dominant_Foot,
                    Nationality, DOB, Player_Position, Overall, Height, Weight
                ) VALUES (
                    :1, :2, :3, :4, :5, :6,
                    TO_DATE(:7, 'DD-MM-YYYY'),
                    :8, :9, :10, :11
                )
                """,
                (
                    player_id,
                    team_id,
                    name,
                    crest,
                    foot,
                    nationality,
                    dob,
                    position,
                    overall,
                    height,
                    weight,
                ),
            )
            if attr_kind == "GK":
                _exec(
                    """
                    INSERT INTO Goalkeeper_Attributes (
                        Player_ID, Diving, Reflexes, Handling,
                        Positioning, Speed, Kicking
                    ) VALUES (:1, :2, :3, :4, :5, :6, :7)
                    """,
                    (player_id, a1, a2, a3, a4, a5, a6),
                )
            else:
                _exec(
                    """
                    INSERT INTO Outfielder_Attributes (
                        Player_ID, Pace, Passing_Rating, Dribbling,
                        Physicality, Defending, Shooting
                    ) VALUES (:1, :2, :3, :4, :5, :6, :7)
                    """,
                    (player_id, a1, a2, a3, a4, a5, a6),
                )

        for row in FIXTURES:
            (
                fixture_id,
                home,
                away,
                match_dt,
                home_score,
                away_score,
                gameweek,
                potm,
                status,
            ) = row
            _exec(
                """
                INSERT INTO Fixtures (
                    Fixture_ID, Home_Team_ID, Away_Team_ID, Match_Date_Time,
                    Home_Score, Away_Score, Gameweek, Player_Of_The_Match,
                    Match_Status
                ) VALUES (
                    :1, :2, :3,
                    TO_DATE(:4, 'DD-MM-YYYY HH24:MI'),
                    :5, :6, :7, :8, :9
                )
                """,
                (
                    fixture_id,
                    home,
                    away,
                    match_dt,
                    home_score,
                    away_score,
                    gameweek,
                    potm,
                    status,
                ),
            )

        for row in PLAYER_STATS:
            _exec(
                """
                INSERT INTO Player_Stats (
                    Player_ID, Fixture_ID, Goals, Assists, Minutes_Played,
                    Yellow_Cards, Red_Cards, Shots_Saved, Goals_Conceded
                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
                """,
                row,
            )

        for row in ACCOLADES:
            _exec(
                """
                INSERT INTO Player_Accolades (Accolade_ID, Player_ID, Accolade_Name)
                VALUES (:1, :2, :3)
                """,
                row,
            )

        connection.commit()
        messages.append(
            f"Populate complete: {inserted} row(s) inserted, "
            f"{skipped} existing row(s) skipped."
        )
        messages.append(
            f"Seed covers {len(STADIUMS)} stadiums, {len(CLUBS)} clubs, "
            f"{len(MANAGERS)} managers, {len(PLAYERS)} players, "
            f"{len(FIXTURES)} fixtures."
        )
    except oracledb.Error as error:
        connection.rollback()
        error_obj, = error.args
        messages.append(f"Populate failed and was rolled back: {error_obj.message}")
    finally:
        cursor.close()

    return messages
