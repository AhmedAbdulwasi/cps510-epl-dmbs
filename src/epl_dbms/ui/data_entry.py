"""Data Entry page: add, edit and delete rows in any EPL table."""

from __future__ import annotations

import datetime as dt

import streamlit as st
import oracledb

from epl_dbms.repositories.data_entry import (
    TABLE_NAMES,
    Column,
    delete_row,
    fetch_rows,
    get_columns,
    insert_row,
    update_row,
)

# Plain-English versions of the Oracle errors a user is most likely to hit.
FRIENDLY_ERRORS = {
    1: "A row with that primary key already exists.",
    1400: "A required field was left empty.",
    2290: "A value breaks one of the table's CHECK rules (for example, Overall must be 1-99).",
    2291: "A foreign key points to a row that doesn't exist (for example, a Team_ID that isn't in Clubs).",
    2292: "Other rows still depend on this one, so it can't be deleted.",
    12899: "A value is too long for its column.",
}

TYPE_HINTS = {"NUMBER": "number", "DATE": "YYYY-MM-DD", "VARCHAR2": "text"}


def _label(column: Column) -> str:
    """Field label: column name, a * if it's required, and the expected type."""
    star = " *" if not column.nullable else ""
    hint = TYPE_HINTS.get(column.data_type, column.data_type)
    return f"{column.name}{star} ({hint})"


def _convert(column: Column, raw: str) -> object:
    """
    Turn what the user typed into the right Python type for Oracle.

    Empty box -> None. NUMBER -> int or float. DATE accepts 2024-08-17 or
    2024-08-17 15:00. Bad input raises ValueError with a message for the user.
    """
    text = raw.strip()
    if text == "":
        return None
    if column.data_type == "NUMBER":
        try:
            number = float(text)
        except ValueError:
            raise ValueError(f"{column.name} must be a number.") from None
        return int(number) if number.is_integer() else number
    if column.data_type == "DATE":
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return dt.datetime.strptime(text, fmt)
            except ValueError:
                continue
        raise ValueError(f"{column.name} must look like 2024-08-17 or 2024-08-17 15:00.")
    return text


def _display(value: object) -> str:
    """Turn a database value back into text for a box (the opposite of _convert)."""
    if value is None:
        return ""
    if isinstance(value, dt.datetime):
        if value.hour or value.minute:
            return value.strftime("%Y-%m-%d %H:%M")
        return value.strftime("%Y-%m-%d")
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def _show_oracle_error(error: oracledb.Error) -> None:
    """Show a plain-English message plus Oracle's own error text."""
    error_obj, = error.args
    friendly = FRIENDLY_ERRORS.get(getattr(error_obj, "code", None), "Oracle rejected the change.")
    st.error(f"{friendly}\n\n`{error_obj.message}`")


def render_data_entry(connection: oracledb.Connection) -> None:
    st.header("Data Entry")
    st.write("Add, edit or delete rows in any table. Fields marked * are required.")

    table = st.selectbox("Choose a table", TABLE_NAMES, key="data_entry_table")
    try:
        columns = get_columns(connection, table)
    except oracledb.Error as error:
        _show_oracle_error(error)
        return
    if not columns:
        st.warning(f"{table} doesn't exist yet. Run Create Tables first.")
        return

    add_tab, edit_tab, delete_tab = st.tabs(["Add", "Edit", "Delete"])
    with add_tab:
        _render_add(connection, table, columns)
    with edit_tab:
        _render_edit(connection, table, columns)
    with delete_tab:
        _render_delete(connection, table, columns)


def _render_add(
    connection: oracledb.Connection,
    table: str,
    columns: list[Column],
) -> None:
    with st.form(f"add_form_{table}", enter_to_submit=False):
        raw_values = {
            column.name: st.text_input(_label(column), key=f"add_{table}_{column.name}")
            for column in columns
        }
        submitted = st.form_submit_button("Add row", type="primary")

    if not submitted:
        return
    try:
        values = {}
        for column in columns:
            value = _convert(column, raw_values[column.name])
            if value is None:
                if not column.nullable:
                    raise ValueError(f"{column.name} is required.")
                # Leave empty optional fields out so the column's DEFAULT applies.
                continue
            values[column.name] = value
        insert_row(connection, table, values)
        st.success(f"Added a new row to {table}. You can see it in Table Browser.")
    except ValueError as error:
        st.error(str(error))
    except oracledb.Error as error:
        _show_oracle_error(error)


def _pick_row(
    connection: oracledb.Connection,
    table: str,
    columns: list[Column],
    action: str,
) -> dict[str, object] | None:
    """Dropdown to choose one row by its primary key. Returns that row as a dict."""
    rows = fetch_rows(connection, table, columns)
    if not rows:
        st.info(f"{table} has no rows yet.")
        return None

    names = [column.name for column in columns]
    key_names = [column.name for column in columns if column.is_key]
    # Show a name next to the ID when the table has one (e.g. "P01 - Bukayo Saka").
    name_column = next(
        (c.name for c in columns if not c.is_key and c.name.endswith("_NAME")),
        None,
    )
    records = [dict(zip(names, row)) for row in rows]

    def describe(record: dict[str, object]) -> str:
        label = " / ".join(_display(record[name]) for name in key_names)
        if name_column and record[name_column]:
            label += f" - {record[name_column]}"
        return label

    # The version number goes up after every delete. A new number gives
    # Streamlit a brand-new dropdown, so it can't keep showing a deleted row.
    version = st.session_state.get("picker_version", 0)
    index = st.selectbox(
        f"Choose the row to {action}",
        range(len(records)),
        format_func=lambda i: describe(records[i]),
        key=f"{action}_pick_{table}_{version}",
    )
    return records[index]


def _render_edit(
    connection: oracledb.Connection,
    table: str,
    columns: list[Column],
) -> None:
    record = _pick_row(connection, table, columns, "edit")
    if record is None:
        return

    key = {c.name: record[c.name] for c in columns if c.is_key}
    row_id = " / ".join(_display(value) for value in key.values())

    with st.form(f"edit_form_{table}_{row_id}", enter_to_submit=False):
        raw_values = {}
        for column in columns:
            box_key = f"edit_{table}_{row_id}_{column.name}"
            current = _display(record[column.name])
            if column.is_key:
                # Primary keys are locked: other tables point to them.
                st.text_input(_label(column), current, disabled=True, key=box_key)
            else:
                raw_values[column.name] = st.text_input(_label(column), current, key=box_key)
        submitted = st.form_submit_button("Save changes", type="primary")

    if not submitted:
        return
    try:
        values = {}
        for column in columns:
            if column.is_key:
                continue
            value = _convert(column, raw_values[column.name])
            if value is None and not column.nullable:
                raise ValueError(f"{column.name} is required.")
            # On Edit, emptying an optional box sets that column to NULL.
            values[column.name] = value
        changed = update_row(connection, table, key, values)
        if changed == 1:
            st.success(f"Saved changes to {table} row {row_id}.")
        else:
            st.warning("That row no longer exists. Pick it again from the list.")
    except ValueError as error:
        st.error(str(error))
    except oracledb.Error as error:
        _show_oracle_error(error)
        

def _render_delete(
    connection: oracledb.Connection,
    table: str,
    columns: list[Column],
) -> None:
    # Show the result of the last delete (saved before the page reloaded).
    message = st.session_state.pop("delete_message", None)
    if message:
        st.success(message)

    record = _pick_row(connection, table, columns, "delete")
    if record is None:
        return

    key = {c.name: record[c.name] for c in columns if c.is_key}
    row_id = " / ".join(_display(value) for value in key.values())

    st.write("This row will be deleted:")
    st.dataframe(
        [{name: _display(value) for name, value in record.items()}],
        hide_index=True,
    )
    st.caption(
        "Rows in other tables that point to this one follow their foreign-key rule: "
        "ON DELETE CASCADE removes them too, ON DELETE SET NULL blanks the link, "
        "and with no rule Oracle blocks the delete."
    )

    # Same safety idea as Drop Tables: tick the box before the button works.
    confirm = st.checkbox(
        f"Yes, delete {table} row {row_id}",
        key=f"delete_confirm_{table}_{row_id}",
    )
    if st.button("Delete row", type="primary", disabled=not confirm, key=f"delete_button_{table}"):
        try:
            deleted = delete_row(connection, table, key)
            if deleted == 1:
                st.session_state["delete_message"] = f"Deleted {table} row {row_id}."
                # Give the row pickers a fresh start (see _pick_row).
                st.session_state["picker_version"] = st.session_state.get("picker_version", 0) + 1
                st.rerun()  # reload so the deleted row disappears from the list
            else:
                st.warning("That row was already gone.")
        except oracledb.Error as error:
            _show_oracle_error(error)