# streamlit_app.py
import streamlit as st
import requests
import pandas as pd

API_BASE = st.sidebar.text_input("API base URL", value="http://localhost:8000")

st.set_page_config(page_title="Book Recommender UI", layout="wide")
st.title("📚 Book Recommender")

# Controls
mode = st.sidebar.radio("Mode", ["Seed index", "Custom description"])

if mode == "Seed index":
    seed_idx = st.sidebar.number_input("Seed index (0-based)", min_value=0, step=1, value=0)
    desc = None
else:
    desc = st.sidebar.text_area("Enter description", value="", height=150)
    seed_idx = None

top_k = st.sidebar.number_input("Number of recommendations", min_value=1, value=10)

if st.sidebar.button("Get recommendations"):
    params = {"top_k": top_k}
    if seed_idx is not None:
        params["seed_idx"] = int(seed_idx)
    if desc:
        params["desc"] = desc

    try:
        with st.spinner("Querying API..."):
            r = requests.get(f"{API_BASE.rstrip('/')}/recommend", params=params, timeout=15)
            r.raise_for_status()
            payload = r.json()
    except Exception as e:
        st.error(f"API request failed: {e}")
        st.stop()

    seed_info = payload.get("seed_info", {})
    results = payload.get("results", [])

    st.subheader("Seed / Query Info")
    st.json(seed_info)

    if not results:
        st.info("No recommendations found.")
    else:
        st.subheader("Recommendations")
        df = pd.DataFrame(results)
        st.dataframe(df[["rank", "idx", "title", "author", "genre", "score"]])
        for item in results:
            st.markdown(f"**{item['rank']}. {item['title']}** — _{item['author']}_  \nGenres: {item['genre']}  \nScore: {item['score']:.3f}")
