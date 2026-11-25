"""Landing page: scorers, assists, recent matches, table shortcuts."""

from __future__ import annotations

import pandas as pd
import streamlit as st
import oracledb

from epl_dbms.repositories.dashboard import (
    fetch_recent_matches,
    fetch_top_assists,
    fetch_top_scorers,
)


def render_home(connection: oracledb.Connection) -> None:
    st.markdown('<div class="hero-brand">English Premier League</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Database Management System — live standings snapshot from Oracle</div>',
        unsafe_allow_html=True,
    )

    col_scorers, col_assists, col_matches = st.columns(3, gap="large")

    with col_scorers:
        st.markdown('<div class="panel"><h3>Scorers</h3>', unsafe_allow_html=True)
        try:
            columns, rows = fetch_top_scorers(connection)
            if rows:
                st.dataframe(
                    pd.DataFrame(rows, columns=columns),
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.caption("No goal data yet. Run Populate Tables.")
        except oracledb.Error as error:
            st.error(f"Could not load scorers:\n\n{error}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_assists:
        st.markdown('<div class="panel"><h3>Assists</h3>', unsafe_allow_html=True)
        try:
            columns, rows = fetch_top_assists(connection)
            if rows:
                st.dataframe(
                    pd.DataFrame(rows, columns=columns),
                    hide_index=True,
                    use_container_width=True,
                )
            else:
                st.caption("No assist data yet. Run Populate Tables.")
        except oracledb.Error as error:
            st.error(f"Could not load assists:\n\n{error}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_matches:
        st.markdown('<div class="panel"><h3>Most Recent Matches</h3>', unsafe_allow_html=True)
        try:
            columns, rows = fetch_recent_matches(connection)
            if not rows:
                st.caption("No fixtures yet. Run Populate Tables.")
            else:
                # columns: Fixture_ID, Match_Date_Time, Home_Club, Away_Club,
                # Home_Score, Away_Score, Gameweek, Match_Status
                for row in rows:
                    home = row[2]
                    away = row[3]
                    home_score = row[4]
                    away_score = row[5]
                    gameweek = row[6]
                    status = row[7]
                    st.markdown(
                        f"""
                        <div class="scoreline">
                            <div class="score">{home_score} - {away_score}</div>
                            <div class="teams">{home} &nbsp;vs&nbsp; {away}</div>
                            <div class="meta">GW {gameweek} · {status}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except oracledb.Error as error:
            st.error(f"Could not load recent matches:\n\n{error}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("Table Browser")
    btn_players, btn_teams, btn_managers = st.columns(3)
    with btn_players:
        if st.button("Players", use_container_width=True, type="primary"):
            st.session_state.nav_page = "Table Browser"
            st.session_state.browser_view = "Players"
            st.rerun()
    with btn_teams:
        if st.button("Teams", use_container_width=True, type="primary"):
            st.session_state.nav_page = "Table Browser"
            st.session_state.browser_view = "Teams"
            st.rerun()
    with btn_managers:
        if st.button("Managers", use_container_width=True, type="primary"):
            st.session_state.nav_page = "Table Browser"
            st.session_state.browser_view = "Managers"
            st.rerun()
