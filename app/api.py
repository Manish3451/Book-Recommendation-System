# app/api.py
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pathlib import Path
import joblib
import logging
import numpy as np
import requests
import os
from sklearn.metrics.pairwise import cosine_similarity

LOG = logging.getLogger("recommender_api")
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")

# GitHub release URL for the model file
MODEL_URL = "https://github.com/Manish3451/Book-Recommendation-System/releases/download/v1.0-model/books_w2v.pkl"
LOCAL_MODEL_PATH = Path("books_w2v.pkl")

def download_model_if_needed():
    """Download model from GitHub release if not present locally"""
    if LOCAL_MODEL_PATH.exists():
        LOG.info("Model file already exists locally")
        return LOCAL_MODEL_PATH
    
    LOG.info("Downloading model from GitHub release...")
    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()
        
        # Create directory if it doesn't exist
        LOCAL_MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(LOCAL_MODEL_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        LOG.info("Model downloaded successfully: %s", LOCAL_MODEL_PATH)
        return LOCAL_MODEL_PATH
        
    except Exception as e:
        LOG.error("Failed to download model: %s", e)
        raise

def load_artifact():
    """Load the model artifact, downloading if necessary"""
    try:
        model_path = download_model_if_needed()
        data = joblib.load(model_path)
        return data["w2v_model"], data["vectors"], data["meta"]
    except Exception as e:
        LOG.error("Failed to load artifact: %s", e)
        raise

# Load artifact at startup
try:
    MODEL, VECTORS, META_DF = load_artifact()
    LOG.info("Loaded artifact successfully: %d rows", len(META_DF))
except Exception as e:
    LOG.exception("Failed to load artifact: %s", e)
    MODEL = VECTORS = META_DF = None

app = FastAPI(title="Book Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecItem(BaseModel):
    rank: int
    idx: int
    title: str
    author: str
    genre: str
    score: float

class RecResponse(BaseModel):
    seed_info: Dict[str, Any]
    results: List[RecItem]

# import helper from your script
from scripts.build_tfidf_and_save import _avg_vector_for_text, _safe_text

@app.get("/health")
async def health():
    ok = MODEL is not None and VECTORS is not None and META_DF is not None
    return {"ok": ok, "rows": len(META_DF) if META_DF is not None else 0}

@app.get("/recommend", response_model=RecResponse)
async def recommend(
    seed_idx: Optional[int] = Query(None, description="index of seed book (0-based)"),
    desc: Optional[str] = Query(None, description="custom description text"),
    top_k: int = Query(10, ge=1, description="number of results"),
):
    if MODEL is None:
        raise HTTPException(status_code=500, detail="Model artifact not loaded on server.")

    if desc is None and seed_idx is None:
        raise HTTPException(status_code=400, detail="Provide either seed_idx or desc.")

    if seed_idx is not None:
        if not (0 <= seed_idx < len(META_DF)):
            raise HTTPException(status_code=400, detail=f"seed_idx {seed_idx} out of range")
        seed_row = META_DF.iloc[seed_idx]
        desc = _safe_text(seed_row.get("description", ""))
        seed_info = {
            "mode": "seed",
            "idx": int(seed_idx),
            "title": _safe_text(seed_row.get("title", "")),
            "author": _safe_text(seed_row.get("authors", "")),
            "genre": _safe_text(seed_row.get("genres", "")),
        }
    else:
        seed_info = {"mode": "custom", "idx": None, "title": "", "author": "", "genre": ""}

    # Build query vector
    qv = _avg_vector_for_text(MODEL, desc).reshape(1, -1)
    if np.linalg.norm(qv) == 0:
        return {"seed_info": seed_info, "results": []}

    sims = cosine_similarity(qv, VECTORS).ravel()
    if seed_info["mode"] == "seed":
        sims[seed_info["idx"]] = -1.0  # exclude self

    order = sims.argsort()[::-1][:top_k]

    results = []
    for rank, idx in enumerate(order, 1):
        row = META_DF.iloc[idx]
        results.append({
            "rank": rank,
            "idx": int(idx),
            "title": _safe_text(row.get("title", "")),
            "author": _safe_text(row.get("authors", "")),
            "genre": _safe_text(row.get("genres", "")),
            "score": float(sims[idx]),
        })

    return {"seed_info": seed_info, "results": results}