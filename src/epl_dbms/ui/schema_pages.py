"""Create Tables and Populate Tables GUI pages."""

from __future__ import annotations

import pandas as pd
import streamlit as st
import oracledb

from epl_dbms.repositories.populate import populate_tables, table_row_counts
from epl_dbms.repositories.schema import CREATE_TABLE_STATEMENTS, create_tables


def render_create_tables(connection: oracledb.Connection) -> None:
    st.header("Create Tables")
    st.write(
        "Creates the full EPL schema (Stadiums → Clubs → Managers / Players → "
        "attributes → Fixtures → Player_Stats → Player_Accolades) in 3NF/BCNF."
    )
    with st.expander("Tables that will be created", expanded=False):
        for name, _ in CREATE_TABLE_STATEMENTS:
            st.write(f"- `{name}`")

    if st.button("Run Create Tables", type="primary"):
        with st.spinner("Creating tables…"):
            try:
                messages = create_tables(connection)
                for message in messages:
                    if message.startswith("Failed"):
                        st.error(message)
                    elif "already exists" in message:
                        st.warning(message)
                    else:
                        st.success(message)
            except oracledb.Error as error:
                st.error(f"Create Tables failed:\n\n{error}")


def render_populate_tables(connection: oracledb.Connection) -> None:
    st.header("Populate Tables")
    st.write(
        "Loads the expanded seed set: 20 clubs/stadiums/managers, 99 players "
        "(P01–P99 fits VARCHAR2(3)), crest/photo URLs, fixtures, match stats, "
        "and accolades."
    )
    st.info(
        "Already-loaded rows are detected quickly and reported as "
        "“already present”. Club crest and player photo URLs are refreshed "
        "even when the row already exists."
    )

    if st.button("Run Populate Tables", type="primary"):
        with st.spinner("Checking existing rows and populating…"):
            try:
                messages = populate_tables(connection)
                for message in messages:
                    if message.startswith("Populate failed"):
                        st.error(message)
                    elif "already present" in message and "0 inserted" in message:
                        st.info(message)
                    elif "already in the database" in message:
                        st.info(message)
                    else:
                        st.success(message)
            except oracledb.Error as error:
                st.error(f"Populate Tables failed:\n\n{error}")

    st.subheader("Current table counts")
    try:
        counts = table_row_counts(connection)
        st.dataframe(
            pd.DataFrame(counts, columns=["Table", "Rows"]),
            hide_index=True,
            use_container_width=True,
        )
    except oracledb.Error as error:
        st.error(f"Could not read table counts:\n\n{error}")


def render_drop_tables_stub() -> None:
    st.header("Drop Tables")
    st.warning(
        "Assigned to your teammate. This menu option is reserved so the "
        "assignment menu stays complete (Drop / Create / Populate / Query / Exit)."
    )
    st.code(
        "\n".join(
            [
                "DROP TABLE PLAYER_ACCOLADES CASCADE CONSTRAINTS;",
                "DROP TABLE PLAYER_STATS CASCADE CONSTRAINTS;",
                "DROP TABLE GOALKEEPER_ATTRIBUTES CASCADE CONSTRAINTS;",
                "DROP TABLE OUTFIELDER_ATTRIBUTES CASCADE CONSTRAINTS;",
                "DROP TABLE PLAYERS CASCADE CONSTRAINTS;",
                "DROP TABLE MANAGERS CASCADE CONSTRAINTS;",
                "DROP TABLE FIXTURES CASCADE CONSTRAINTS;",
                "DROP TABLE CLUBS CASCADE CONSTRAINTS;",
                "DROP TABLE STADIUMS CASCADE CONSTRAINTS;",
            ]
        ),
        language="sql",
    )


def render_data_entry_stub() -> None:
    st.header("Data Entry")
    st.warning(
        "Assigned to your teammate. This section should let users insert, "
        "update, delete, and search records across each table/form for the "
        "bonus 'separate access to the form and tables' marks."
    )
    st.write(
        "Table Browser (already implemented) covers read/search. Data Entry "
        "should add write operations per table."
    )
