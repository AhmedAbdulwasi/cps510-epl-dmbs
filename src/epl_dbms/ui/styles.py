"""Shared Streamlit CSS for the EPL DBMS interface."""

APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Source+Sans+3:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(0, 210, 120, 0.12), transparent 35%),
        linear-gradient(160deg, #07111f 0%, #10243d 45%, #0b1726 100%);
    color: #f4f7fb;
}

h1, h2, h3, .hero-brand {
    font-family: 'Oswald', sans-serif;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.hero-brand {
    font-size: 2.4rem;
    margin-bottom: 0.15rem;
    color: #f7fbff;
}

.hero-sub {
    color: #a9bdd6;
    margin-bottom: 1.0rem;
}

.panel {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 0.85rem 0.95rem 1rem;
}

.panel-compact {
    min-height: 0;
}

.panel h3 {
    margin-top: 0;
    margin-bottom: 0.65rem;
    color: #7dffb3;
}

.leader-row {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.4rem 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.leader-row:last-child {
    border-bottom: none;
}

.leader-row img.photo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    object-position: top center;
    background: #d9e2ec;
    border: 1px solid rgba(125, 255, 179, 0.35);
}

.leader-row img.crest {
    width: 22px;
    height: 22px;
    object-fit: contain;
}

.leader-meta {
    flex: 1;
    min-width: 0;
}

.leader-meta .name {
    font-weight: 700;
    color: #f4f7fb;
    line-height: 1.15;
}

.leader-meta .club {
    color: #9bb0c7;
    font-size: 0.82rem;
}

.leader-stat {
    font-family: 'Oswald', sans-serif;
    font-size: 1.25rem;
    color: #7dffb3;
    min-width: 1.5rem;
    text-align: right;
}

.scoreline {
    text-align: center;
    padding: 0.55rem 0.35rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.scoreline:last-child {
    border-bottom: none;
}

.scoreline .crests {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.2rem;
}

.scoreline .crests img {
    width: 34px;
    height: 34px;
    object-fit: contain;
}

.scoreline .score {
    font-family: 'Oswald', sans-serif;
    font-size: 1.55rem;
    line-height: 1;
    color: #ffffff;
}

.scoreline .teams {
    margin-top: 0.2rem;
    color: #c5d4e7;
    font-size: 0.85rem;
}

.scoreline .meta {
    color: #7f93ac;
    font-size: 0.75rem;
}

div[data-testid="stSidebar"] {
    background: #081427;
}

div[data-testid="stSidebar"] * {
    color: #e8eef7;
}
</style>
"""


def inject_styles() -> None:
    import streamlit as st

    st.markdown(APP_CSS, unsafe_allow_html=True)
