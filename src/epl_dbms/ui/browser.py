"""Table Browser page for all nine schema tables."""

from __future__ import annotations

import pandas as pd
import streamlit as st
import oracledb

from epl_dbms.repositories.browser import TABLE_VIEWS, fetch_table, normalize_view
from epl_dbms.repositories.populate import table_row_counts


IMAGE_COLUMNS = {
    "Crest",
    "Photo",
    "Club_Crest",
    "Home_Crest",
    "Away_Crest",
}


def render_table_browser(connection: oracledb.Connection) -> None:
    st.header("Table Browser")
    st.write("Browse and search all nine tables in the EPL schema.")

    views = list(TABLE_VIEWS.keys())
    current = normalize_view(st.session_state.get("browser_view", "Players"))
    if current not in views:
        current = "Players"
    # Keep the selectbox key in sync with Home shortcut on_click handlers.
    st.session_state.browser_view = current

    view = st.selectbox(
        "Choose a table",
        views,
        key="browser_view",
    )

    search = st.text_input(
        "Search",
        placeholder="Filter by name, ID, club, status…",
        key="browser_search",
    )

    try:
        columns, rows = fetch_table(connection, view, search)
        data = pd.DataFrame(rows, columns=columns)
        st.caption(f"{len(data)} record(s) in `{view}`")

        column_config = {}
        for col in data.columns:
            if col in IMAGE_COLUMNS:
                column_config[col] = st.column_config.ImageColumn(col, width="small")
            elif col == "Crest" or str(col).endswith("Crest"):
                column_config[col] = st.column_config.ImageColumn(str(col), width="small")

        st.dataframe(
            data,
            hide_index=True,
            use_container_width=True,
            column_config=column_config or None,
        )
    except oracledb.Error as error:
        st.error(f"Could not load {view}:\n\n{error}")
        st.info(
            "If tables are missing, run Create Tables then Populate Tables from the sidebar."
        )

    with st.expander("Row counts for all tables"):
        try:
            counts = table_row_counts(connection)
            count_df = pd.DataFrame(counts, columns=["Table", "Rows"])
            st.dataframe(count_df, hide_index=True, use_container_width=True)
        except oracledb.Error as error:
            st.error(f"Could not read table counts:\n\n{error}")

    if st.button("Refresh"):
        st.rerun()
