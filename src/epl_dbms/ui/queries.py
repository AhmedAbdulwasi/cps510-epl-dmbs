"""Query Tables page — predefined advanced reports."""

from __future__ import annotations

import pandas as pd
import streamlit as st
import oracledb

from epl_dbms.repositories.queries import QUERY_TABLES, fetch_query_results


def render_query_tables(connection: oracledb.Connection) -> None:
    st.header("Query Tables")
    st.write(
        "Run the assignment's predefined reports (joins, set operations, "
        "aggregates, EXISTS, and statistics)."
    )

    query_name = st.selectbox("Choose a predefined query", list(QUERY_TABLES))
    with st.expander("SQL for selected query"):
        st.code(QUERY_TABLES[query_name].strip(), language="sql")

    if st.button("Run Query", type="primary"):
        try:
            columns, rows = fetch_query_results(connection, QUERY_TABLES[query_name])
            results = pd.DataFrame(rows, columns=columns)
            st.caption(f"{len(results)} row(s)")
            st.dataframe(results, hide_index=True, use_container_width=True)
        except oracledb.Error as error:
            st.error(f"Could not run the selected query:\n\n{error}")
