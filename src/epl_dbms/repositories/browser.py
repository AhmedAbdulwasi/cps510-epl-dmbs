"""Table Browser queries for Players, Clubs (Teams), and Managers."""

from __future__ import annotations

import oracledb

PLAYERS_QUERY = """
    SELECT p.Player_ID,
           p.Player_Name,
           c.Club_Name,
           p.Player_Position,
           p.Nationality,
           p.Overall,
           p.Dominant_Foot,
           p.Height,
           p.Weight,
           TO_CHAR(p.DOB, 'YYYY-MM-DD') AS DOB
    FROM Players p
    LEFT JOIN Clubs c ON c.Team_ID = p.Team_ID
    WHERE (
        :search IS NULL
        OR UPPER(p.Player_Name) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(c.Club_Name) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(p.Player_Position) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(p.Nationality) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(p.Player_ID) LIKE '%' || UPPER(:search) || '%'
    )
    ORDER BY p.Player_Name
"""

TEAMS_QUERY = """
    SELECT c.Team_ID,
           c.Club_Name,
           c.City,
           c.Stadium_Name,
           s.Stadium_Capacity,
           c.Year_Founded,
           c.Valuation
    FROM Clubs c
    LEFT JOIN Stadiums s ON s.Stadium_Name = c.Stadium_Name
    WHERE (
        :search IS NULL
        OR UPPER(c.Club_Name) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(c.City) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(c.Stadium_Name) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(c.Team_ID) LIKE '%' || UPPER(:search) || '%'
    )
    ORDER BY c.Club_Name
"""

MANAGERS_QUERY = """
    SELECT m.Manager_ID,
           m.Manager_Name,
           c.Club_Name,
           m.Preferred_Formation,
           m.Trophies,
           m.Salary,
           TO_CHAR(m.Date_Joining, 'YYYY-MM-DD') AS Date_Joining,
           TO_CHAR(m.Contract_Expiry_Date, 'YYYY-MM-DD') AS Contract_Expiry,
           TO_CHAR(m.DOB, 'YYYY-MM-DD') AS DOB
    FROM Managers m
    LEFT JOIN Clubs c ON c.Team_ID = m.Team_ID
    WHERE (
        :search IS NULL
        OR UPPER(m.Manager_Name) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(c.Club_Name) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(m.Manager_ID) LIKE '%' || UPPER(:search) || '%'
        OR UPPER(m.Preferred_Formation) LIKE '%' || UPPER(:search) || '%'
    )
    ORDER BY m.Manager_Name
"""


def _fetch_with_search(
    connection: oracledb.Connection,
    query: str,
    search: str | None,
) -> tuple[list[str], list[tuple[object, ...]]]:
    cursor = connection.cursor()
    try:
        term = search.strip() if search and search.strip() else None
        cursor.execute(query, search=term)
        columns = [description[0] for description in cursor.description]
        return columns, cursor.fetchall()
    finally:
        cursor.close()


def fetch_players(
    connection: oracledb.Connection,
    search: str | None = None,
) -> tuple[list[str], list[tuple[object, ...]]]:
    return _fetch_with_search(connection, PLAYERS_QUERY, search)


def fetch_teams(
    connection: oracledb.Connection,
    search: str | None = None,
) -> tuple[list[str], list[tuple[object, ...]]]:
    return _fetch_with_search(connection, TEAMS_QUERY, search)


def fetch_managers(
    connection: oracledb.Connection,
    search: str | None = None,
) -> tuple[list[str], list[tuple[object, ...]]]:
    return _fetch_with_search(connection, MANAGERS_QUERY, search)
