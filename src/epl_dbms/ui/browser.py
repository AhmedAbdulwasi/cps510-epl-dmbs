"""Table Browser page for Players, Teams, and Managers."""

from __future__ import annotations

import pandas as pd
import streamlit as st
import oracledb

from epl_dbms.repositories.browser import fetch_managers, fetch_players, fetch_teams


VIEWS = ("Players", "Teams", "Managers")


def render_table_browser(connection: oracledb.Connection) -> None:
    st.header("Table Browser")
    st.write("Browse and search core tables. Use the filters to find specific records.")

    default_view = st.session_state.get("browser_view", "Players")
    if default_view not in VIEWS:
        default_view = "Players"

    view = st.radio(
        "Choose a table",
        VIEWS,
        horizontal=True,
        index=VIEWS.index(default_view),
        key="browser_view_radio",
    )
    st.session_state.browser_view = view

    search = st.text_input(
        "Search",
        placeholder="Name, club, position, nationality, ID…",
        key="browser_search",
    )

    try:
        if view == "Players":
            columns, rows = fetch_players(connection, search)
        elif view == "Teams":
            columns, rows = fetch_teams(connection, search)
        else:
            columns, rows = fetch_managers(connection, search)

        data = pd.DataFrame(rows, columns=columns)
        st.caption(f"{len(data)} record(s)")
        st.dataframe(data, hide_index=True, use_container_width=True)
    except oracledb.Error as error:
        st.error(f"Could not load {view}:\n\n{error}")
        st.info(
            "If tables are missing, run Create Tables then Populate Tables from the sidebar."
        )

    if st.button("Refresh"):
        st.rerun()
