import oracledb

QUERY_TABLES = {
    "Managers without fast outfielders": """
        SELECT Team_ID AS "TEAM ID"
        FROM Managers
        WHERE Team_ID IS NOT NULL
        MINUS
        SELECT p.Team_ID
        FROM Players p
        JOIN Outfielder_Attributes o ON o.Player_ID = p.Player_ID
        WHERE o.Pace >= 80
    """,
    "Club average goals and assists": """
        SELECT c.Club_Name AS "CLUB",
               ROUND(AVG(s.Goals + s.Assists), 1) AS "AVERAGE G/A",
               COUNT(p.Player_ID) AS "TOTAL PLAYERS"
        FROM Clubs c
        JOIN Players p ON p.Team_ID = c.Team_ID
        JOIN Player_Stats s ON s.Player_ID = p.Player_ID
        GROUP BY c.Club_Name
        HAVING AVG(s.Goals + s.Assists) >= 0.5
        ORDER BY "AVERAGE G/A" DESC
    """,
    "Players with accolades and goals": """
        SELECT p.Player_ID, p.Player_Name
        FROM Players p
        WHERE EXISTS (
            SELECT *
            FROM Player_Accolades a
            WHERE a.Player_ID = p.Player_ID
        )
        AND EXISTS (
            SELECT *
            FROM Player_Stats s
            WHERE s.Player_ID = p.Player_ID AND s.Goals > 0
        )
    """,
    "Clubs above average player rating": """
        SELECT c.Club_Name,
               ROUND(AVG(p.Overall), 2) AS Avg_Rating
        FROM Clubs c
        JOIN Players p ON c.Team_ID = p.Team_ID
        GROUP BY c.Club_Name
        HAVING AVG(p.Overall) > (SELECT AVG(Overall) FROM Players)
        ORDER BY Avg_Rating DESC
    """,
    "Club valuation statistics": """
        SELECT MIN(Valuation) AS Minimum_Value,
               MAX(Valuation) AS Maximum_Value,
               ROUND(AVG(Valuation), 2) AS Average_Value,
               ROUND(VARIANCE(Valuation), 2) AS Variance_Value,
               ROUND(STDDEV(Valuation), 2) AS Std_Deviation
        FROM Clubs
    """,
}


def fetch_query_results(connection: oracledb.Connection, query: str,) -> tuple[list[str], list[tuple[object, ...]]]:
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        return columns, cursor.fetchall()
    finally:
        cursor.close()
