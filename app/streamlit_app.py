# streamlit_app.py (replace your current file with this)
import streamlit as st
import requests
import pandas as pd

# MUST be the first Streamlit command executed in the app
st.set_page_config(page_title="Book Recommender UI", layout="wide")

# UI header
st.title("📚 Book Recommender")

# Sidebar inputs (after set_page_config)
API_BASE = st.sidebar.text_input("API base URL", value="http://localhost:8000")
mode = st.sidebar.radio("Mode", ["Seed index", "Custom description"])

if mode == "Seed index":
    seed_idx = st.sidebar.number_input("Seed index (0-based)", min_value=0, step=1, value=0)
    desc = None
else:
    desc = st.sidebar.text_area("Enter description", value="", height=150)
    seed_idx = None

top_k = st.sidebar.number_input("Number of recommendations", min_value=1, value=10)

def fetch_recommendations(api_base: str, params: dict, timeout: int = 15):
    """Query the API and return parsed JSON or raise."""
    url = f"{api_base.rstrip('/')}/recommend"
    resp = requests.get(url, params=params, timeout=timeout)
    resp.raise_for_status()
    return resp.json()

if st.sidebar.button("Get recommendations"):
    params = {"top_k": int(top_k)}
    if seed_idx is not None:
        params["seed_idx"] = int(seed_idx)
    if desc:
        params["desc"] = desc

    try:
        with st.spinner("Querying API..."):
            payload = fetch_recommendations(API_BASE, params)
    except Exception as e:
        st.error(f"API request failed: {e}")
    else:
        seed_info = payload.get("seed_info", {})
        results = payload.get("results", [])

        st.subheader("Seed / Query Info")
        st.json(seed_info)

        if not results:
            st.info("No recommendations found.")
        else:
            st.subheader("Recommendations")
            df = pd.DataFrame(results)
            # show only columns we expect (guard if missing)
            cols = [c for c in ["rank", "idx", "title", "author", "genre", "score"] if c in df.columns]
            st.dataframe(df[cols])

            for item in results:
                title = item.get("title", "—")
                author = item.get("author", "")
                genre = item.get("genre", "")
                score = item.get("score", 0.0)
                st.markdown(f"**{item.get('rank', '?')}. {title}** — _{author}_  \nGenres: {genre}  \nScore: {score:.3f}")
