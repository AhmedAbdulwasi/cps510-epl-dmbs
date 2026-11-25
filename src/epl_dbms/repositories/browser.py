"""Table Browser queries for all nine EPL schema tables."""

from __future__ import annotations

import oracledb

TABLE_VIEWS: dict[str, str] = {
    "Stadiums": """
        SELECT Stadium_Name, Stadium_Capacity
        FROM Stadiums
        WHERE (
            :search IS NULL
            OR UPPER(Stadium_Name) LIKE '%' || UPPER(:search) || '%'
        )
        ORDER BY Stadium_Name
    """,
    "Clubs": """
        SELECT c.Team_ID,
               c.Club_Name,
               c.Crest,
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
    """,
    "Managers": """
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
    """,
    "Players": """
        SELECT p.Player_ID,
               p.Crest AS Photo,
               p.Player_Name,
               c.Club_Name,
               c.Crest AS Club_Crest,
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
    """,
    "Goalkeeper_Attributes": """
        SELECT g.Player_ID,
               p.Player_Name,
               g.Diving,
               g.Reflexes,
               g.Handling,
               g.Positioning,
               g.Speed,
               g.Kicking
        FROM Goalkeeper_Attributes g
        LEFT JOIN Players p ON p.Player_ID = g.Player_ID
        WHERE (
            :search IS NULL
            OR UPPER(g.Player_ID) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(p.Player_Name) LIKE '%' || UPPER(:search) || '%'
        )
        ORDER BY p.Player_Name
    """,
    "Outfielder_Attributes": """
        SELECT o.Player_ID,
               p.Player_Name,
               o.Pace,
               o.Passing_Rating,
               o.Dribbling,
               o.Physicality,
               o.Defending,
               o.Shooting
        FROM Outfielder_Attributes o
        LEFT JOIN Players p ON p.Player_ID = o.Player_ID
        WHERE (
            :search IS NULL
            OR UPPER(o.Player_ID) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(p.Player_Name) LIKE '%' || UPPER(:search) || '%'
        )
        ORDER BY p.Player_Name
    """,
    "Fixtures": """
        SELECT f.Fixture_ID,
               TO_CHAR(f.Match_Date_Time, 'YYYY-MM-DD HH24:MI') AS Match_Date_Time,
               home.Club_Name AS Home_Club,
               away.Club_Name AS Away_Club,
               home.Crest AS Home_Crest,
               away.Crest AS Away_Crest,
               f.Home_Score,
               f.Away_Score,
               f.Gameweek,
               f.Player_Of_The_Match,
               f.Match_Status
        FROM Fixtures f
        JOIN Clubs home ON home.Team_ID = f.Home_Team_ID
        JOIN Clubs away ON away.Team_ID = f.Away_Team_ID
        WHERE (
            :search IS NULL
            OR UPPER(home.Club_Name) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(away.Club_Name) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(f.Fixture_ID) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(f.Match_Status) LIKE '%' || UPPER(:search) || '%'
        )
        ORDER BY f.Match_Date_Time DESC NULLS LAST, f.Fixture_ID
    """,
    "Player_Stats": """
        SELECT s.Player_ID,
               p.Player_Name,
               s.Fixture_ID,
               s.Goals,
               s.Assists,
               s.Minutes_Played,
               s.Yellow_Cards,
               s.Red_Cards,
               s.Shots_Saved,
               s.Goals_Conceded
        FROM Player_Stats s
        LEFT JOIN Players p ON p.Player_ID = s.Player_ID
        WHERE (
            :search IS NULL
            OR UPPER(s.Player_ID) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(p.Player_Name) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(s.Fixture_ID) LIKE '%' || UPPER(:search) || '%'
        )
        ORDER BY s.Fixture_ID, s.Player_ID
    """,
    "Player_Accolades": """
        SELECT a.Accolade_ID,
               a.Player_ID,
               p.Player_Name,
               a.Accolade_Name
        FROM Player_Accolades a
        LEFT JOIN Players p ON p.Player_ID = a.Player_ID
        WHERE (
            :search IS NULL
            OR UPPER(a.Accolade_ID) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(a.Player_ID) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(p.Player_Name) LIKE '%' || UPPER(:search) || '%'
            OR UPPER(a.Accolade_Name) LIKE '%' || UPPER(:search) || '%'
        )
        ORDER BY a.Accolade_ID
    """,
}

# Friendly aliases used by Home shortcuts
TABLE_ALIASES = {
    "Teams": "Clubs",
}


def normalize_view(view: str) -> str:
    return TABLE_ALIASES.get(view, view)


def fetch_table(
    connection: oracledb.Connection,
    view: str,
    search: str | None = None,
) -> tuple[list[str], list[tuple[object, ...]]]:
    table = normalize_view(view)
    query = TABLE_VIEWS[table]
    cursor = connection.cursor()
    try:
        term = search.strip() if search and search.strip() else None
        cursor.execute(query, search=term)
        columns = [description[0] for description in cursor.description]
        return columns, cursor.fetchall()
    finally:
        cursor.close()
