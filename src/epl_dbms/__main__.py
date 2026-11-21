import pandas as pd
import streamlit as st
import oracledb

from epl_dbms.database import connect
from epl_dbms.repositories.clubs import CLUB_COLUMNS, fetch_clubs
from epl_dbms.settings import OracleSettings


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

    st.sidebar.title("EPL Database")
    page = st.sidebar.radio("Navigation", ["Clubs", "Table Browser", "Data Entry", "Reports", "Views"],)

    if "oracle_settings" not in st.session_state:
        try:
            st.session_state.oracle_settings = OracleSettings.from_environment()
        except ValueError as error:
            st.session_state.oracle_settings = None
            st.error(str(error))
            st.info(
                "PLEASE SET ORACLE_USER, ORACLE_PASSWORD, and ORACLE_DSN in the environment (within the terminal or in a .env file)"
                "before starting Streamlit."
            )
            st.stop()

    settings = st.session_state.oracle_settings

    st.title("CPS510 English Premier League DBMS")

    if "oracle_connection" not in st.session_state:
        try:
            st.session_state.oracle_connection = connect(settings)
        except oracledb.Error as error:
            st.sidebar.error("Oracle connection failed")
            st.error(f"Could not connect to Oracle:\n\n{error}")
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

    if page == "Clubs":
        st.header("Clubs")

        try:
            rows = fetch_clubs(settings, connection)
            data = pd.DataFrame(rows, columns=CLUB_COLUMNS)
            st.dataframe(data, use_container_width=True, hide_index=True)
            st.caption(f"{len(data)} club(s) loaded")
        except oracledb.Error as error:
            st.error(f"Could not load the Clubs table:\n\n{error}")
        else:
            if st.button("Refresh", type="primary"):
                st.rerun()
    else:
        st.header(page)
        st.info("Soon... This page is under construction.")


if __name__ == "__main__":
    main()
