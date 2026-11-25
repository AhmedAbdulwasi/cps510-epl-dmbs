"""Landing page: scorers, assists, recent matches, table shortcuts."""

from __future__ import annotations

import html
import streamlit as st
import oracledb

from epl_dbms.repositories.browser import TABLE_VIEWS
from epl_dbms.repositories.dashboard import (
    fetch_recent_matches,
    fetch_top_assists,
    fetch_top_scorers,
)


def _go_browser(view: str) -> None:
    """on_click callback — safe to set nav_page before the radio is created."""
    st.session_state.nav_page = "Table Browser"
    st.session_state.browser_view = view


def _img(url: object, css_class: str, alt: str) -> str:
    if not url or not str(url).startswith("http"):
        return ""
    safe = html.escape(str(url), quote=True)
    return f'<img class="{css_class}" src="{safe}" alt="{html.escape(alt)}" />'


def _render_leaderboard(rows: list[tuple], stat_label: str) -> None:
    # row: Player, Club, Stat, Photo, Club_Crest
    for row in rows:
        player, club, stat, photo, club_crest = row
        st.markdown(
            f"""
            <div class="leader-row">
                {_img(photo, "photo", str(player))}
                {_img(club_crest, "crest", str(club))}
                <div class="leader-meta">
                    <div class="name">{html.escape(str(player))}</div>
                    <div class="club">{html.escape(str(club))}</div>
                </div>
                <div class="leader-stat" title="{stat_label}">{stat}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_home(connection: oracledb.Connection) -> None:
    st.markdown('<div class="hero-brand">English Premier League</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">Database Management System — live standings snapshot from Oracle</div>',
        unsafe_allow_html=True,
    )

    col_scorers, col_assists, col_matches = st.columns(3, gap="medium")

    with col_scorers:
        st.markdown('<div class="panel panel-compact"><h3>Scorers</h3>', unsafe_allow_html=True)
        try:
            _, rows = fetch_top_scorers(connection)
            if rows:
                _render_leaderboard(rows, "Goals")
            else:
                st.caption("No goal data yet. Run Populate Tables.")
        except oracledb.Error as error:
            st.error(f"Could not load scorers:\n\n{error}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_assists:
        st.markdown('<div class="panel panel-compact"><h3>Assists</h3>', unsafe_allow_html=True)
        try:
            _, rows = fetch_top_assists(connection)
            if rows:
                _render_leaderboard(rows, "Assists")
            else:
                st.caption("No assist data yet. Run Populate Tables.")
        except oracledb.Error as error:
            st.error(f"Could not load assists:\n\n{error}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_matches:
        st.markdown(
            '<div class="panel panel-compact"><h3>Most Recent Matches</h3>',
            unsafe_allow_html=True,
        )
        try:
            _, rows = fetch_recent_matches(connection)
            if not rows:
                st.caption("No fixtures yet. Run Populate Tables.")
            else:
                # Fixture_ID, Match_Date_Time, Home, Away, HS, AS, GW, Status, HomeCrest, AwayCrest
                for row in rows:
                    home = row[2]
                    away = row[3]
                    home_score = row[4]
                    away_score = row[5]
                    gameweek = row[6]
                    status = row[7]
                    home_crest = row[8]
                    away_crest = row[9]
                    st.markdown(
                        f"""
                        <div class="scoreline">
                            <div class="crests">
                                {_img(home_crest, "", str(home))}
                                <span class="score">{home_score} - {away_score}</span>
                                {_img(away_crest, "", str(away))}
                            </div>
                            <div class="teams">{html.escape(str(home))} vs {html.escape(str(away))}</div>
                            <div class="meta">GW {gameweek} · {html.escape(str(status))}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except oracledb.Error as error:
            st.error(f"Could not load recent matches:\n\n{error}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.subheader("Table Browser")
    st.caption("Jump to any of the nine schema tables.")

    labels = list(TABLE_VIEWS.keys())
    # Keep Teams alias button as well for the wireframe
    shortcut_labels = ["Players", "Clubs", "Managers"] + [
        name for name in labels if name not in {"Players", "Clubs", "Managers"}
    ]

    rows_of_buttons = [
        shortcut_labels[0:3],
        shortcut_labels[3:6],
        shortcut_labels[6:9],
    ]
    for button_row in rows_of_buttons:
        cols = st.columns(len(button_row))
        for col, label in zip(cols, button_row):
            with col:
                st.button(
                    "Teams" if label == "Clubs" else label.replace("_", " "),
                    use_container_width=True,
                    type="primary",
                    key=f"home_goto_{label}",
                    on_click=_go_browser,
                    args=(label,),
                )
