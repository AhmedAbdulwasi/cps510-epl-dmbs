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
    margin-bottom: 1.4rem;
}

.panel {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 1rem 1.1rem 1.2rem;
    min-height: 320px;
}

.panel h3 {
    margin-top: 0;
    margin-bottom: 0.85rem;
    color: #7dffb3;
}

.scoreline {
    text-align: center;
    padding: 0.85rem 0.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.scoreline .score {
    font-family: 'Oswald', sans-serif;
    font-size: 2rem;
    line-height: 1;
    color: #ffffff;
}

.scoreline .teams {
    margin-top: 0.35rem;
    color: #c5d4e7;
    font-size: 0.95rem;
}

.scoreline .meta {
    color: #7f93ac;
    font-size: 0.8rem;
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
