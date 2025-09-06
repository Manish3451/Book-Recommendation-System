from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Tuple, Dict

import joblib
import numpy as np
import pandas as pd

from gensim.models import Word2Vec
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

import nltk
import re 

# ---------------- Dependencies / Notes ----------------
# Requires: gensim, nltk, scikit-learn, joblib, pandas, numpy
# If you don't have NLTK data installed run once:
# >>> import nltk
# >>> nltk.download('punkt')
# >>> nltk.download('wordnet')
# >>> nltk.download('omw-1.4')

# ---------------- Paths / Config ----------------
DATA_PATH = Path(r"data/books.csv")
OUT_PKL = Path("data/books_w2v.pkl")

# Split configuration (Top-10 = 5 by desc, 3 by genre, 2 by title)
SEED_IDX = 0
TOP_DESC = 5
TOP_GENRE = 3
TOP_TITLE = 2





# Word2Vec training hyperparams (kept small/simple for speed)
W2V_PARAMS = {
    "vector_size": 100,
    "window": 5,
    "min_count": 2,
    "workers": 1,
    "epochs": 5,
    "seed": 42,
}

# Preprocessing switches
USE_LEMMATIZE = True
USE_STEM = False
REMOVE_SHORT = True  # drop tokens shorter than 2 chars

LOG_FILE = "logs/recommender.log"


# ---------------- Logging ----------------
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------- Helpers ----------------
_lemmatizer = WordNetLemmatizer()
_stemmer = PorterStemmer()


def _safe_text(x) -> str:
    if x is None:
        return ""
    s = str(x)
    return "" if s.lower() == "nan" else s

def _ensure_nltk_data():
    """Ensure punkt/punkt_tab and wordnet are available. Try to download if not."""
    try:
        # try common packages used in this script
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        try:
            nltk.download("punkt", quiet=True)
        except Exception:
            logger.warning("Unable to download 'punkt' via nltk. Will use fallback tokenizer.")
    # some installations may request 'punkt_tab' (your error suggested this)
    try:
        nltk.data.find("tokenizers/punkt_tab/english")
    except LookupError:
        try:
            nltk.download("punkt_tab", quiet=True)
        except Exception:
            # not critical; fallback exists
            logger.debug("'punkt_tab' not available; continuing and relying on fallback if needed.")

    # wordnet for lemmatizer
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        try:
            nltk.download("wordnet", quiet=True)
            nltk.download("omw-1.4", quiet=True)
        except Exception:
            logger.warning("Unable to download 'wordnet' data; lemmatization may fail.")

# call once at import/run time
try:
    _ensure_nltk_data()
except Exception as e:
    # don't crash — we'll fallback later
    logger.debug("NLTK data check failed: %s", e)

def safe_tokenize(text: str) -> List[str]:
    """Try NLTK's word_tokenize, fall back to a simple regex tokenization if unavailable."""
    if not text:
        return []
    try:
        # prefer nltk tokenizer if available & resources were downloaded
        return word_tokenize(text)
    except Exception:
        # fallback: return alphabetic tokens only (simple and robust)
        return re.findall(r"[a-zA-Z]+", text.lower())

def preprocess_text(text: str) -> List[str]:
    """Simple, robust preprocessing pipeline.

    - tokenizes (NLTK)
    - lowercases
    - optional lemmatize/stem
    - drops short tokens
    """
    if not text:
        return []
    # naive lowering + tokenization
    tokens = word_tokenize(text.lower())

    out: List[str] = []
    for t in tokens:
        # keep only alphabetic tokens (simple filter)
        if not t.isalpha():
            continue
        if REMOVE_SHORT and len(t) < 2:
            continue
        tok = t
        if USE_LEMMATIZE:
            tok = _lemmatizer.lemmatize(tok)
        if USE_STEM:
            tok = _stemmer.stem(tok)
        out.append(tok)
    return out


def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="utf-8")
    logger.info("Original shape: %s", df.shape)

    expected = ["title", "authors", "description", "genres"]
    for col in expected:
        if col not in df.columns:
            df[col] = ""

    df = df[expected]
    df["description"] = df["description"].astype(str)
    df = df.dropna(subset=["description"])
    df = df[df["description"].str.strip() != ""]

    if len(df) > 5000:
        df = df.sample(n=5000, random_state=42)

    df = df.reset_index(drop=True)
    logger.info("After cleaning: %s", df.shape)
    return df


def build_word2vec(df: pd.DataFrame, params: dict = W2V_PARAMS) -> Tuple[Word2Vec, np.ndarray]:
    """Train Word2Vec on the descriptions and return (model, vectors_matrix).

    Vectors matrix: each row corresponds to the averaged word vectors for that row's description.
    """
    logger.info("Preprocessing text for Word2Vec training...")
    corpus = [preprocess_text(t) for t in df["description"].astype(str)]

    # Simple guard: if many empty after preprocessing, consider lowering min_count or disabling filters
    empty_count = sum(1 for s in corpus if not s)
    if empty_count > 0:
        logger.warning("%d documents empty after preprocessing (they will get zero vectors)", empty_count)

    logger.info("Training Word2Vec (small, fast settings)...")
    model = Word2Vec(sentences=corpus, **params)

    # Build averaged vectors (rows x dim)
    dim = model.vector_size
    vectors = np.zeros((len(corpus), dim), dtype=float)

    for i, tokens in enumerate(corpus):
        if not tokens:
            continue
        vecs = [model.wv[t] for t in tokens if t in model.wv]
        if not vecs:
            continue
        vectors[i] = np.mean(vecs, axis=0)

    # simple diagnostics
    nonzero = np.sum(np.linalg.norm(vectors, axis=1) > 0)
    logger.info("Built averaged vectors: shape=%s | nonzero rows=%d/%d", vectors.shape, nonzero, len(vectors))
    return model, vectors


def save_artifact(model: Word2Vec, vectors: np.ndarray, df: pd.DataFrame, out_path: Path = OUT_PKL) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"w2v_model": model, "vectors": vectors, "meta": df}
    joblib.dump(payload, out_path)
    logger.info("Saved payload to %s", out_path)


def load_artifact(out_path: Path = OUT_PKL):
    if not out_path.exists():
        raise FileNotFoundError(f"Artifact not found at: {out_path}")
    data = joblib.load(out_path)
    return data["w2v_model"], data["vectors"], data["meta"]


def _avg_vector_for_text(model: Word2Vec, text: str) -> np.ndarray:
    tokens = preprocess_text(text)
    if not tokens:
        return np.zeros(model.vector_size)
    vecs = [model.wv[t] for t in tokens if t in model.wv]
    if not vecs:
        return np.zeros(model.vector_size)
    return np.mean(vecs, axis=0)

def recommend_split(
    seed_idx: int | None = SEED_IDX,
    *,
    desc_query: str | None = None,
    top_k: int = 10,
    dedupe: bool = True,
):
    data = joblib.load(OUT_PKL)
    model = data["w2v_model"]
    vectors = data["vectors"]
    df = data["meta"]
    n = len(df)

    # If no description given, fall back to seed_idx
    if desc_query is None:
        if seed_idx is None:
            raise ValueError("Provide either desc_query or seed_idx.")
        if not (0 <= seed_idx < n):
            raise IndexError(f"seed_idx {seed_idx} out of range 0..{n-1}")

        seed_row = df.iloc[seed_idx]
        desc_query = _safe_text(seed_row.get("description", ""))
        seed_info = {
            "mode": "seed",
            "idx": int(seed_idx),
            "title": _safe_text(seed_row.get("title", "")),
            "author": _safe_text(seed_row.get("authors", "")),
            "genre": _safe_text(seed_row.get("genres", "")),
        }
    else:
        seed_info = {
            "mode": "custom",
            "idx": None,
            "title": "",
            "author": "",
            "genre": "",
        }

    # Build query vector
    qv = _avg_vector_for_text(model, desc_query).reshape(1, -1)
    if np.linalg.norm(qv) == 0:
        return seed_info, []

    sims = cosine_similarity(qv, vectors).ravel()
    if seed_info["mode"] == "seed":
        sims[seed_info["idx"]] = -1.0  # exclude self

    order = sims.argsort()[::-1][:top_k]

    results = []
    for rank, idx in enumerate(order, 1):
        row = df.iloc[idx]
        results.append({
            "rank": rank,
            "idx": int(idx),
            "title": _safe_text(row.get("title", "")),
            "author": _safe_text(row.get("authors", "")),
            "genre": _safe_text(row.get("genres", "")),
            "score": float(sims[idx]),
        })

    return seed_info, results



def main():
    df = load_data(DATA_PATH)
    model, vectors = build_word2vec(df)
    save_artifact(model, vectors, df, OUT_PKL)
    logger.info("Finished building artifacts. You can now call recommend_split(...) or run the script with a seed.")


if __name__ == "__main__":
    main()
    # immediately run recommendations using SEED_IDX
    try:
        recommend_split(seed_idx=SEED_IDX)
    except Exception as e:
        logger.exception("Error during recommend_split: %s", e)
