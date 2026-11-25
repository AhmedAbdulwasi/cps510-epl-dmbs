"""CPS510 English Premier League DBMS — Streamlit entry point."""

from __future__ import annotations

import streamlit as st
import oracledb

from epl_dbms.database import connect
from epl_dbms.settings import OracleSettings
from epl_dbms.ui.browser import render_table_browser
from epl_dbms.ui.data_entry import render_data_entry
from epl_dbms.ui.home import render_home
from epl_dbms.ui.queries import render_query_tables
from epl_dbms.ui.schema_pages import (
    render_create_tables,
    render_drop_tables,
    render_populate_tables,
)
from epl_dbms.ui.styles import inject_styles

# Rubric menu options plus landing / browser extras.
MENU_OPTIONS = [
    "Home",
    "Create Tables",
    "Populate Tables",
    "Query Tables",
    "Table Browser",
    "Drop Tables",
    "Data Entry",
    "Exit",
]


def render_connection_status(connection: oracledb.Connection) -> None:
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT 1 FROM DUAL")
        cursor.fetchone()
    finally:
        cursor.close()


def main() -> None:
    st.set_page_config(
        page_title="CPS510 EPL DBMS",
        page_icon="⚽",
        layout="wide",
    )
    inject_styles()

    if "nav_page" not in st.session_state:
        st.session_state.nav_page = "Home"
    if "browser_view" not in st.session_state:
        st.session_state.browser_view = "Players"

    st.sidebar.title("EPL Database")
    # key="nav_page" lets Home shortcut buttons set the active menu item.
    page = st.sidebar.radio(
        "Navigation",
        MENU_OPTIONS,
        key="nav_page",
    )

    if page == "Exit":
        connection = st.session_state.get("oracle_connection")
        close_error = None
        if connection is not None:
            try:
                connection.close()
            except oracledb.Error as error:
                close_error = error
        st.session_state.clear()
        if close_error is not None:
            st.error(f"Could not close Oracle cleanly:\n\n{close_error}")
        else:
            st.success("Oracle session closed.")
        st.info(
            "This ends the app's database session for this browser tab. "
            "Please close this browser tab when you are finished — Streamlit "
            "keeps the local web server running until you stop it in the terminal "
            "(Ctrl+C)."
        )
        st.stop()

    if "oracle_settings" not in st.session_state:
        try:
            st.session_state.oracle_settings = OracleSettings.from_environment()
        except ValueError as error:
            st.session_state.oracle_settings = None
            st.error(str(error))
            st.info(
                "Set ORACLE_USER, ORACLE_PASSWORD, and ORACLE_DSN in the "
                "environment or a .env file before starting Streamlit."
            )
            st.stop()

    settings = st.session_state.oracle_settings

    if "oracle_connection" not in st.session_state:
        try:
            st.session_state.oracle_connection = connect(settings)
        except oracledb.Error as error:
            st.sidebar.error("Oracle connection failed")
            st.error(f"Could not connect to Oracle:\n\n{error}")
            st.info(
                "If SQL Developer went stale, reconnect on the CS VPN and "
                "refresh this page."
            )
            st.stop()

    connection = st.session_state.oracle_connection
    try:
        render_connection_status(connection)
        st.sidebar.success("Oracle connected")
    except oracledb.Error as error:
        st.session_state.pop("oracle_connection", None)
        st.sidebar.error("Oracle connection lost")
        st.error(f"Oracle connection failed:\n\n{error}")
        st.stop()

    if page == "Home":
        render_home(connection)
    elif page == "Create Tables":
        render_create_tables(connection)
    elif page == "Populate Tables":
        render_populate_tables(connection)
    elif page == "Query Tables":
        render_query_tables(connection)
    elif page == "Table Browser":
        render_table_browser(connection)
    elif page == "Drop Tables":
        render_drop_tables(connection)
    elif page == "Data Entry":
        render_data_entry(connection)


if __name__ == "__main__":
    main()
