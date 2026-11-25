"""Read-only dashboard queries for the landing page."""

from __future__ import annotations

import oracledb


TOP_SCORERS_QUERY = """
    SELECT p.Player_Name AS Player,
           c.Club_Name AS Club,
           NVL(SUM(s.Goals), 0) AS Goals
    FROM Players p
    JOIN Clubs c ON c.Team_ID = p.Team_ID
    LEFT JOIN Player_Stats s ON s.Player_ID = p.Player_ID
    GROUP BY p.Player_Name, c.Club_Name
    HAVING NVL(SUM(s.Goals), 0) > 0
    ORDER BY Goals DESC, p.Player_Name
    FETCH FIRST 10 ROWS ONLY
"""

TOP_ASSISTS_QUERY = """
    SELECT p.Player_Name AS Player,
           c.Club_Name AS Club,
           NVL(SUM(s.Assists), 0) AS Assists
    FROM Players p
    JOIN Clubs c ON c.Team_ID = p.Team_ID
    LEFT JOIN Player_Stats s ON s.Player_ID = p.Player_ID
    GROUP BY p.Player_Name, c.Club_Name
    HAVING NVL(SUM(s.Assists), 0) > 0
    ORDER BY Assists DESC, p.Player_Name
    FETCH FIRST 10 ROWS ONLY
"""

RECENT_MATCHES_QUERY = """
    SELECT f.Fixture_ID,
           f.Match_Date_Time,
           home.Club_Name AS Home_Club,
           away.Club_Name AS Away_Club,
           f.Home_Score,
           f.Away_Score,
           f.Gameweek,
           f.Match_Status
    FROM Fixtures f
    JOIN Clubs home ON home.Team_ID = f.Home_Team_ID
    JOIN Clubs away ON away.Team_ID = f.Away_Team_ID
    ORDER BY f.Match_Date_Time DESC NULLS LAST, f.Fixture_ID DESC
    FETCH FIRST 8 ROWS ONLY
"""


def _fetch(
    connection: oracledb.Connection,
    query: str,
) -> tuple[list[str], list[tuple[object, ...]]]:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        return columns, cursor.fetchall()
    finally:
        cursor.close()


def fetch_top_scorers(
    connection: oracledb.Connection,
) -> tuple[list[str], list[tuple[object, ...]]]:
    return _fetch(connection, TOP_SCORERS_QUERY)


def fetch_top_assists(
    connection: oracledb.Connection,
) -> tuple[list[str], list[tuple[object, ...]]]:
    return _fetch(connection, TOP_ASSISTS_QUERY)


def fetch_recent_matches(
    connection: oracledb.Connection,
) -> tuple[list[str], list[tuple[object, ...]]]:
    return _fetch(connection, RECENT_MATCHES_QUERY)
