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


def _existing_keys(
    cursor: oracledb.Cursor,
    sql: str,
) -> set[object]:
    cursor.execute(sql)
    return {row[0] for row in cursor.fetchall()}


def _existing_pairs(
    cursor: oracledb.Cursor,
    sql: str,
) -> set[tuple[object, object]]:
    cursor.execute(sql)
    return {(row[0], row[1]) for row in cursor.fetchall()}


def populate_tables(connection: oracledb.Connection) -> list[str]:
    """
    Insert seed rows in FK-safe order.

    Existing primary keys are detected with SELECTs (fast) rather than
    relying on unique-constraint exceptions. Crest/photo URLs on existing
    Clubs and Players rows are refreshed so the Home page can show images.
    """
    messages: list[str] = []
    cursor = connection.cursor()

    try:
        existing_stadiums = _existing_keys(cursor, "SELECT Stadium_Name FROM Stadiums")
        existing_clubs = _existing_keys(cursor, "SELECT Team_ID FROM Clubs")
        existing_managers = _existing_keys(cursor, "SELECT Manager_ID FROM Managers")
        existing_players = _existing_keys(cursor, "SELECT Player_ID FROM Players")
        existing_gk = _existing_keys(cursor, "SELECT Player_ID FROM Goalkeeper_Attributes")
        existing_of = _existing_keys(cursor, "SELECT Player_ID FROM Outfielder_Attributes")
        existing_fixtures = _existing_keys(cursor, "SELECT Fixture_ID FROM Fixtures")
        existing_stats = _existing_pairs(
            cursor,
            "SELECT Player_ID, Fixture_ID FROM Player_Stats",
        )
        existing_accolades = _existing_keys(cursor, "SELECT Accolade_ID FROM Player_Accolades")

        def report(label: str, inserted: int, skipped: int, updated: int = 0) -> None:
            parts = [f"{label}: {inserted} inserted", f"{skipped} already present"]
            if updated:
                parts.append(f"{updated} image URL(s) refreshed")
            messages.append(" · ".join(parts) + ".")

        # --- Stadiums ---
        inserted = skipped = 0
        for stadium_name, capacity in STADIUMS:
            if stadium_name in existing_stadiums:
                skipped += 1
                continue
            cursor.execute(
                "INSERT INTO Stadiums (Stadium_Name, Stadium_Capacity) VALUES (:1, :2)",
                (stadium_name, capacity),
            )
            inserted += 1
        report("Stadiums", inserted, skipped)

        # --- Clubs (refresh Crest URLs on existing rows) ---
        inserted = skipped = updated = 0
        for row in CLUBS:
            team_id, club_name, valuation, stadium, year, crest, city = row
            if team_id in existing_clubs:
                cursor.execute(
                    "UPDATE Clubs SET Crest = :crest WHERE Team_ID = :team_id",
                    {"crest": crest, "team_id": team_id},
                )
                skipped += 1
                updated += 1
                continue
            cursor.execute(
                """
                INSERT INTO Clubs (
                    Team_ID, Club_Name, Valuation, Stadium_Name,
                    Year_Founded, Crest, City
                ) VALUES (:1, :2, :3, :4, :5, :6, :7)
                """,
                row,
            )
            inserted += 1
        report("Clubs", inserted, skipped, updated)

        # --- Managers ---
        inserted = skipped = 0
        for row in MANAGERS:
            manager_id = row[0]
            if manager_id in existing_managers:
                skipped += 1
                continue
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
            cursor.execute(
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
            inserted += 1
        report("Managers", inserted, skipped)

        # --- Players + attributes (refresh photo URLs on existing rows) ---
        inserted = skipped = updated = 0
        attr_inserted = attr_skipped = 0
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
            if player_id in existing_players:
                cursor.execute(
                    "UPDATE Players SET Crest = :crest WHERE Player_ID = :player_id",
                    {"crest": crest, "player_id": player_id},
                )
                skipped += 1
                updated += 1
            else:
                cursor.execute(
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
                inserted += 1

            if attr_kind == "GK":
                if player_id in existing_gk:
                    attr_skipped += 1
                else:
                    cursor.execute(
                        """
                        INSERT INTO Goalkeeper_Attributes (
                            Player_ID, Diving, Reflexes, Handling,
                            Positioning, Speed, Kicking
                        ) VALUES (:1, :2, :3, :4, :5, :6, :7)
                        """,
                        (player_id, a1, a2, a3, a4, a5, a6),
                    )
                    attr_inserted += 1
                    existing_gk.add(player_id)
            else:
                if player_id in existing_of:
                    attr_skipped += 1
                else:
                    cursor.execute(
                        """
                        INSERT INTO Outfielder_Attributes (
                            Player_ID, Pace, Passing_Rating, Dribbling,
                            Physicality, Defending, Shooting
                        ) VALUES (:1, :2, :3, :4, :5, :6, :7)
                        """,
                        (player_id, a1, a2, a3, a4, a5, a6),
                    )
                    attr_inserted += 1
                    existing_of.add(player_id)

        report("Players", inserted, skipped, updated)
        report("Player attributes (GK/OF)", attr_inserted, attr_skipped)

        # --- Fixtures ---
        inserted = skipped = 0
        for row in FIXTURES:
            fixture_id = row[0]
            if fixture_id in existing_fixtures:
                skipped += 1
                continue
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
            cursor.execute(
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
            inserted += 1
        report("Fixtures", inserted, skipped)

        # --- Player_Stats ---
        inserted = skipped = 0
        for row in PLAYER_STATS:
            key = (row[0], row[1])
            if key in existing_stats:
                skipped += 1
                continue
            cursor.execute(
                """
                INSERT INTO Player_Stats (
                    Player_ID, Fixture_ID, Goals, Assists, Minutes_Played,
                    Yellow_Cards, Red_Cards, Shots_Saved, Goals_Conceded
                ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)
                """,
                row,
            )
            inserted += 1
        report("Player_Stats", inserted, skipped)

        # --- Accolades ---
        inserted = skipped = 0
        for row in ACCOLADES:
            if row[0] in existing_accolades:
                skipped += 1
                continue
            cursor.execute(
                """
                INSERT INTO Player_Accolades (Accolade_ID, Player_ID, Accolade_Name)
                VALUES (:1, :2, :3)
                """,
                row,
            )
            inserted += 1
        report("Player_Accolades", inserted, skipped)

        connection.commit()

        total_new = sum(
            int(msg.split(":")[1].split()[0])
            for msg in messages
            if "inserted" in msg
        )
        if total_new == 0:
            messages.insert(
                0,
                "All seed rows are already in the database — nothing new to insert. "
                "Club crest and player photo URLs were refreshed where needed.",
            )
        else:
            messages.insert(
                0,
                f"Populate finished — {total_new} new row(s) inserted across tables.",
            )
    except oracledb.Error as error:
        connection.rollback()
        error_obj, = error.args
        messages.append(f"Populate failed and was rolled back: {error_obj.message}")
    finally:
        cursor.close()

    return messages


def table_row_counts(connection: oracledb.Connection) -> list[tuple[str, int]]:
    """Return (table_name, row_count) for all nine schema tables."""
    tables = [
        "Stadiums",
        "Clubs",
        "Managers",
        "Players",
        "Goalkeeper_Attributes",
        "Outfielder_Attributes",
        "Fixtures",
        "Player_Stats",
        "Player_Accolades",
    ]
    cursor = connection.cursor()
    counts: list[tuple[str, int]] = []
    try:
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                counts.append((table, int(cursor.fetchone()[0])))
            except oracledb.Error:
                counts.append((table, -1))
    finally:
        cursor.close()
    return counts
