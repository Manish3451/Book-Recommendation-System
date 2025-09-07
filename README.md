# Book Recommendation System

> A full-stack Book Recommendation System powered by Word2Vec embeddings and cosine similarity. FastAPI backend, Streamlit frontend, Dockerized and ready for deployment.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Technologies](#technologies)
* [Getting Started](#getting-started)

  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Run Locally (Development)](#run-locally-development)
  * [Run with Docker](#run-with-docker)
* [Usage](#usage)

  * [Web Interface](#web-interface)
  * [API Usage](#api-usage)
  * [Example Queries](#example-queries)
* [API Documentation](#api-documentation)

  * `POST /recommend`
  * `GET /health`
  * `GET /stats`
* [Project Structure](#project-structure)
* [Configuration](#configuration)
* [Data](#data)
* [Testing](#testing)
* [Contributing](#contributing)
* [License](#license)

---

## Overview

This project provides book recommendations using Word2Vec embeddings (to embed book descriptions) and cosine similarity (to find nearest neighbors). It exposes a FastAPI backend for recommendation queries and a Streamlit frontend for an interactive UI. The system is containerized with Docker and ready to deploy (e.g., Render, Heroku, or your preferred provider).

## Features

* Text-based recommendations from natural-language descriptions
* Configurable number of recommendations (1–20)
* FastAPI REST API with health and stats endpoints
* Streamlit web UI for quick experimentation
* Model serialization for fast startup
* Dockerfile for easy containerization

## Technologies

* Python 3.11+
* FastAPI (backend)
* Uvicorn (ASGI server)
* Streamlit (frontend)
* Gensim (Word2Vec)
* scikit-learn (cosine similarity)
* pandas / NumPy
* joblib (model serialization)
* Docker

## Getting Started

### Prerequisites

* Python 3.11 or later
* pip (or pipx)
* Docker (optional, for containerized runs)

### Installation

```bash
# clone the repo
git clone https://github.com/Manish3451/Book-Recommendation-System.git
cd Book-Recommendation-System

# create venv and activate
python -m venv .venv
# Windows
# .venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

### Run Locally (Development)

Run backend (FastAPI + Uvicorn):

```bash
# from project root
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run Streamlit frontend (default port 8501):

```bash
streamlit run app/frontend.py --server.port 8501
```

Open the Streamlit app at: `http://localhost:8501`

> If you prefer to run both with a single command, consider using `tmux`, `make`, or a small shell script.

### Run with Docker

Build the image and run containers (example):

```bash
# build image
docker build -t book-recs:latest .

# run container (exposes 8000)
docker run -p 8000:8000 book-recs:latest
```

If using docker-compose a `docker-compose.yml` may run both backend and frontend on their respective ports.

---

# 📸 Architecture Diagrams ------------------------ 
### System Architecture 
![System Architecture](app/static/images/system-architecture.png)

### Model Architecture 
![Model Architecture](app/static/images/model-architecture.png)

## Usage


Open the Streamlit app at `http://localhost:8501`.

Choose your input method:

* Enter a book description in the text area
* Or select a book index from the dataset

Then:

1. Set number of recommendations (1–20)
2. Click **Get Recommendations**
3. View results in table and list format

### API Usage

**Python example**

```python
import requests

# Get recommendations by description
response = requests.post("http://localhost:8000/recommend", json={
    "description": "A young wizard battles dark forces",
    "num_recommendations": 5
})

recommendations = response.json()
print(recommendations)
```

### Example Queries

Try these sample descriptions:

* "A detective solving mysterious crimes in Victorian London"
* "Space exploration and alien civilizations"
* "Romance novel set in medieval times"
* "Coming of age story about friendship"

---

## API Documentation

### `POST /recommend`

Get book recommendations based on description.

**Request Body (JSON)**

```json
{
  "description": "string",
  "num_recommendations": 5
}
```

**Response (JSON)**

```json
{
  "recommendations": [
    {
      "title": "Book Title",
      "author": "Author Name",
      "genre": "Genre",
      "similarity_score": 0.95,
      "description": "Book description..."
    }
  ],
  "query": "original query",
  "total_found": 5
}
```

### `GET /health`

Health check endpoint.

**Response**

```json
{ "status": "healthy" }
```

### `GET /stats`

Get system statistics.

**Response**

```json
{
  "total_books": 1000,
  "uptime": "2h 30m",
  "requests_served": 150
}
```

---

## Project Structure

A suggested project layout — adapt to your repo:

```
book-recommendation-system/
├── app/
│   ├── main.py            # FastAPI app entrypoint
│   ├── api.py             # route definitions
│   ├── model.py           # model loading & inference helpers
│   ├── utils.py           # utility functions
│   ├── frontend.py        # Streamlit front-end (if inside same repo)
│   └── data/
│       ├── books.csv
│       └── embeddings.joblib
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── tests/
    └── test_api.py
```

---

## Configuration

Use environment variables for configurable parameters (example):

* `PORT` — backend port (default: `8000`)
* `MODEL_PATH` — path to serialized embeddings or model
* `DATA_PATH` — path to dataset (CSV)

Example `.env` file:

```env
PORT=8000
MODEL_PATH=app/data/embeddings.joblib
DATA_PATH=app/data/books.csv
```

---

## Data

* `books.csv` should contain at minimum: `title, author, genre, description`.
* Precompute embeddings for all descriptions and serialize them (e.g., with `joblib`) for fast lookup.

Tips:

* Keep a mapping `index -> book metadata` and a `NumPy` matrix of embeddings for similarity search.
* Normalize and clean text before training Word2Vec (lowercase, remove punctuation, strip stopwords as appropriate).

---

## Testing

Run unit tests with `pytest`:

```bash
pytest -q
```

Include tests for:

* API response shapes
* Similarity ranking sanity checks
* Model loading and health checks

---

## Contributing

Contributions welcome! Please open an issue or pull request with a clear description of changes.

Suggested workflow:

1. Fork the repo
2. Create a feature branch `feat/your-feature`
3. Commit and push
4. Open a Pull Request with a description and tests

---

## License

This project is provided under the MIT License. See the `LICENSE` file for details.

---

*Made with ❤️ — happy recommending!*
