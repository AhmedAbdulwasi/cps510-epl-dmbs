"""Read-only queries for the Clubs table."""

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


def fetch_clubs(settings: OracleSettings) -> list[tuple[object, ...]]:
    """Return all Clubs rows for the initial read-only UI."""
    connection = connect(settings)
    try:
        cursor = connection.cursor()
        try:
            cursor.execute(CLUBS_QUERY)
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        connection.close()
