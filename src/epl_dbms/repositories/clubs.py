from epl_dbms.database import connect
from epl_dbms.settings import OracleSettings

CLUB_COLUMNS = (
    "Team_ID",
    "Club_Name",
    "Valuation",
    "Stadium_Name",
    "Year_Founded",
    "City",
)

CLUBS_QUERY = """
    SELECT Team_ID, Club_Name, Valuation, Stadium_Name, Year_Founded, City
    FROM Clubs
    ORDER BY Team_ID
"""


def fetch_clubs(
    settings: OracleSettings,
    connection=None,
) -> list[tuple[object, ...]]:
    owns_connection = connection is None
    if owns_connection:
        connection = connect(settings)
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(CLUBS_QUERY)
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        if owns_connection:
            connection.close()
