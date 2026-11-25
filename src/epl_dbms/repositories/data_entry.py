"""Data Entry: add, edit and delete rows in any of the nine EPL tables."""

from __future__ import annotations

from dataclasses import dataclass

import oracledb

from epl_dbms.repositories.schema import CREATE_TABLE_STATEMENTS

# The only table names that can ever reach the SQL below. They come from
# Create Tables, never from anything the user types.
TABLE_NAMES = [name for name, _ in CREATE_TABLE_STATEMENTS]


@dataclass
class Column:
    name: str
    data_type: str  # NUMBER, VARCHAR2 or DATE
    nullable: bool  # False means the column is required (NOT NULL)
    is_key: bool  # True if the column is part of the primary key


def _check_table(table: str) -> None:
    if table not in TABLE_NAMES:
        raise ValueError(f"Unknown table: {table}")


def get_columns(connection: oracledb.Connection, table: str) -> list[Column]:
    """
    Read a table's columns from Oracle's catalog (the data dictionary).

    USER_TAB_COLUMNS gives every column with its type and whether it allows
    NULL. USER_CONSTRAINTS + USER_CONS_COLUMNS tell us which columns make up
    the primary key. Because the forms are built from the catalog, they
    always match the real tables.
    """
    _check_table(table)
    cursor = connection.cursor()
    try:
        cursor.execute(
            """
            SELECT cc.column_name
            FROM user_constraints c
            JOIN user_cons_columns cc ON cc.constraint_name = c.constraint_name
            WHERE c.table_name = :table_name
              AND c.constraint_type = 'P'
            """,
            table_name=table.upper(),
        )
        key_columns = {row[0] for row in cursor.fetchall()}

        cursor.execute(
            """
            SELECT column_name, data_type, nullable
            FROM user_tab_columns
            WHERE table_name = :table_name
            ORDER BY column_id
            """,
            table_name=table.upper(),
        )
        return [
            Column(name, data_type, nullable == "Y", name in key_columns)
            for name, data_type, nullable in cursor.fetchall()
        ]
    finally:
        cursor.close()


def insert_row(
    connection: oracledb.Connection,
    table: str,
    values: dict[str, object],
) -> None:
    """
    INSERT one row.

    Column names come from the catalog (get_columns). The values the user
    typed are sent separately as bind variables (:1, :2, ...), so they are
    never pasted into the SQL text. That is what blocks SQL injection.
    """
    _check_table(table)
    columns = list(values)
    placeholders = ", ".join(f":{i + 1}" for i in range(len(columns)))
    sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    cursor = connection.cursor()
    try:
        cursor.execute(sql, list(values.values()))
        connection.commit()
    finally:
        cursor.close()


def fetch_rows(
    connection: oracledb.Connection,
    table: str,
    columns: list[Column],
) -> list[tuple[object, ...]]:
    """Every row of the table, sorted by primary key, for the Edit/Delete pickers."""
    _check_table(table)
    names = ", ".join(column.name for column in columns)
    order_by = ", ".join(column.name for column in columns if column.is_key) or "1"
    cursor = connection.cursor()
    try:
        cursor.execute(f"SELECT {names} FROM {table} ORDER BY {order_by}")
        return cursor.fetchall()
    finally:
        cursor.close()


def update_row(
    connection: oracledb.Connection,
    table: str,
    key: dict[str, object],
    values: dict[str, object],
) -> int:
    """
    UPDATE one row, found by its primary key.

    SET changes only the non-key columns. WHERE matches every primary-key
    column (Player_Stats needs two: Player_ID AND Fixture_ID). Returns how
    many rows changed, which should be exactly 1.
    """
    _check_table(table)
    set_part = ", ".join(f"{name} = :{i + 1}" for i, name in enumerate(values))
    offset = len(values)
    where_part = " AND ".join(
        f"{name} = :{offset + i + 1}" for i, name in enumerate(key)
    )
    sql = f"UPDATE {table} SET {set_part} WHERE {where_part}"
    cursor = connection.cursor()
    try:
        cursor.execute(sql, list(values.values()) + list(key.values()))
        changed = cursor.rowcount
        connection.commit()
        return changed
    finally:
        cursor.close()


def delete_row(
    connection: oracledb.Connection,
    table: str,
    key: dict[str, object],
) -> int:
    """
    DELETE one row, found by its primary key. Returns how many rows went (should be 1).

    Rows in other tables that point to this one follow their foreign-key rule:
    ON DELETE CASCADE removes them too (deleting a player removes their stats),
    ON DELETE SET NULL blanks the link (a manager's Team_ID), and with no rule
    Oracle refuses with ORA-02292 (a club that still has fixtures).
    """
    _check_table(table)
    where_part = " AND ".join(f"{name} = :{i + 1}" for i, name in enumerate(key))
    cursor = connection.cursor()
    try:
        cursor.execute(f"DELETE FROM {table} WHERE {where_part}", list(key.values()))
        deleted = cursor.rowcount
        connection.commit()
        return deleted
    finally:
        cursor.close()