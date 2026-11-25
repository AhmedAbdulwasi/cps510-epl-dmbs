"""DDL helpers for creating the EPL schema (3NF / BCNF)."""

from __future__ import annotations

import oracledb

# Matches the team's BCNF/3NF draft. Player_ID is VARCHAR2(3) (P01-P99),
# so Populate caps the roster at 99 players.
CREATE_TABLE_STATEMENTS: list[tuple[str, str]] = [
    (
        "Stadiums",
        """
        CREATE TABLE Stadiums (
            Stadium_Name VARCHAR2(50) PRIMARY KEY,
            Stadium_Capacity NUMBER CHECK (Stadium_Capacity > 0)
        )
        """,
    ),
    (
        "Clubs",
        """
        CREATE TABLE Clubs (
            Team_ID VARCHAR2(2) PRIMARY KEY,
            Club_Name VARCHAR2(40) NOT NULL,
            Valuation NUMBER DEFAULT 0,
            Stadium_Name VARCHAR2(50),
            Year_Founded NUMBER(4) CHECK (Year_Founded > 1864),
            Crest VARCHAR2(400),
            City VARCHAR2(30),
            FOREIGN KEY (Stadium_Name) REFERENCES Stadiums (Stadium_Name)
        )
        """,
    ),
    (
        "Managers",
        """
        CREATE TABLE Managers (
            Manager_ID VARCHAR2(2) PRIMARY KEY,
            Manager_Name VARCHAR2(50) NOT NULL,
            Team_ID VARCHAR2(2),
            Date_Joining DATE,
            Contract_Expiry_Date DATE,
            Trophies NUMBER(3) DEFAULT 0,
            Salary NUMBER(9) DEFAULT 0,
            DOB DATE,
            Preferred_Formation VARCHAR2(3),
            FOREIGN KEY (Team_ID) REFERENCES Clubs (Team_ID) ON DELETE SET NULL
        )
        """,
    ),
    (
        "Players",
        """
        CREATE TABLE Players (
            Player_ID VARCHAR2(3) PRIMARY KEY,
            Team_ID VARCHAR2(2),
            Player_Name VARCHAR2(50) NOT NULL,
            Crest VARCHAR2(400),
            Dominant_Foot VARCHAR2(1),
            Nationality VARCHAR2(3),
            DOB DATE,
            Player_Position VARCHAR2(3),
            Overall NUMBER(2) CHECK (Overall BETWEEN 1 AND 99),
            Height NUMBER(3),
            Weight NUMBER(3),
            FOREIGN KEY (Team_ID) REFERENCES Clubs (Team_ID) ON DELETE CASCADE
        )
        """,
    ),
    (
        "Goalkeeper_Attributes",
        """
        CREATE TABLE Goalkeeper_Attributes (
            Player_ID VARCHAR2(3) PRIMARY KEY,
            Diving NUMBER(2) CHECK (Diving BETWEEN 1 AND 99),
            Reflexes NUMBER(2) CHECK (Reflexes BETWEEN 1 AND 99),
            Handling NUMBER(2) CHECK (Handling BETWEEN 1 AND 99),
            Positioning NUMBER(2) CHECK (Positioning BETWEEN 1 AND 99),
            Speed NUMBER(2) CHECK (Speed BETWEEN 1 AND 99),
            Kicking NUMBER(2) CHECK (Kicking BETWEEN 1 AND 99),
            FOREIGN KEY (Player_ID) REFERENCES Players (Player_ID) ON DELETE CASCADE
        )
        """,
    ),
    (
        "Outfielder_Attributes",
        """
        CREATE TABLE Outfielder_Attributes (
            Player_ID VARCHAR2(3) PRIMARY KEY,
            Pace NUMBER(2) CHECK (Pace BETWEEN 1 AND 99),
            Passing_Rating NUMBER(2) CHECK (Passing_Rating BETWEEN 1 AND 99),
            Dribbling NUMBER(2) CHECK (Dribbling BETWEEN 1 AND 99),
            Physicality NUMBER(2) CHECK (Physicality BETWEEN 1 AND 99),
            Defending NUMBER(2) CHECK (Defending BETWEEN 1 AND 99),
            Shooting NUMBER(2) CHECK (Shooting BETWEEN 1 AND 99),
            FOREIGN KEY (Player_ID) REFERENCES Players (Player_ID) ON DELETE CASCADE
        )
        """,
    ),
    (
        "Fixtures",
        """
        CREATE TABLE Fixtures (
            Fixture_ID VARCHAR2(3) PRIMARY KEY,
            Home_Team_ID VARCHAR2(2) NOT NULL,
            Away_Team_ID VARCHAR2(2) NOT NULL,
            Match_Date_Time DATE,
            Home_Score NUMBER(2) DEFAULT 0,
            Away_Score NUMBER(2) DEFAULT 0,
            Gameweek NUMBER(2) DEFAULT 0,
            Player_Of_The_Match VARCHAR2(3),
            Match_Status VARCHAR2(20),
            FOREIGN KEY (Home_Team_ID) REFERENCES Clubs (Team_ID),
            FOREIGN KEY (Away_Team_ID) REFERENCES Clubs (Team_ID),
            CONSTRAINT Diff_Teams CHECK (Home_Team_ID != Away_Team_ID),
            FOREIGN KEY (Player_Of_The_Match)
                REFERENCES Players (Player_ID) ON DELETE SET NULL
        )
        """,
    ),
    (
        "Player_Stats",
        """
        CREATE TABLE Player_Stats (
            Player_ID VARCHAR2(3),
            Fixture_ID VARCHAR2(3),
            Goals NUMBER(2) DEFAULT 0,
            Assists NUMBER(2) DEFAULT 0,
            Minutes_Played NUMBER(3) DEFAULT 0,
            Yellow_Cards NUMBER(1) DEFAULT 0,
            Red_Cards NUMBER(1) DEFAULT 0,
            Shots_Saved NUMBER(3) DEFAULT 0,
            Goals_Conceded NUMBER(2) DEFAULT 0,
            PRIMARY KEY (Player_ID, Fixture_ID),
            FOREIGN KEY (Player_ID) REFERENCES Players (Player_ID) ON DELETE CASCADE,
            FOREIGN KEY (Fixture_ID) REFERENCES Fixtures (Fixture_ID) ON DELETE CASCADE
        )
        """,
    ),
    (
        "Player_Accolades",
        """
        CREATE TABLE Player_Accolades (
            Accolade_ID VARCHAR2(3) PRIMARY KEY,
            Player_ID VARCHAR2(3) NOT NULL,
            Accolade_Name VARCHAR2(70) NOT NULL,
            FOREIGN KEY (Player_ID) REFERENCES Players (Player_ID) ON DELETE CASCADE
        )
        """,
    ),
]


def create_tables(connection: oracledb.Connection) -> list[str]:
    """
    Create all schema tables in dependency order.

    Returns a list of human-readable status lines (created / already exists / error).
    """
    messages: list[str] = []
    cursor = connection.cursor()
    try:
        for table_name, ddl in CREATE_TABLE_STATEMENTS:
            try:
                cursor.execute(ddl)
                messages.append(f"Created table {table_name}.")
            except oracledb.Error as error:
                error_obj, = error.args
                # ORA-00955: name is already used by an existing object
                if getattr(error_obj, "code", None) == 955:
                    messages.append(f"Table {table_name} already exists (skipped).")
                else:
                    messages.append(f"Failed to create {table_name}: {error_obj.message}")
        connection.commit()
    finally:
        cursor.close()
    return messages
