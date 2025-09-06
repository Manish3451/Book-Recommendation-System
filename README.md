# 📚 Book Recommendation System

This project implements a **Book Recommendation System** that suggests books to users based on their preferences. The system leverages natural language processing (NLP) techniques, specifically **Word2Vec**, to understand book similarities and provide relevant recommendations. It features a **FastAPI backend**, a **Streamlit frontend**, and is deployable with Docker and Render.

---

## 📑 Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## ✨ Features
- **Content-Based Recommendations**: Suggests books based on their descriptions using semantic similarity.
- **Interactive Web Interface**: A user-friendly UI built with Streamlit.
- **Scalable API**: FastAPI backend for efficient recommendation serving.
- **Word2Vec Embeddings**: Generates dense semantic vector representations for books.
- **Cosine Similarity**: Measures similarity between book embeddings for recommendations.

---

## 🏗️ System Architecture

The system follows a layered design to ensure modularity, scalability, and maintainability.

```mermaid
flowchart TB
  subgraph UI["🎨 Frontend Layer"]
    U[User] --> S[Streamlit Web App]
  end

  subgraph API["⚡ API Layer"]
    S --> A[FastAPI API Server]
    A --> R[/recommend Endpoint/]
  end

  subgraph ML["🧠 ML Model Layer"]
    R --> W2V[Word2Vec Model]
    W2V --> E[Book Embeddings]
    E --> CS[Cosine Similarity]
  end

  subgraph Data["🗂️ Data Layer"]
    CS --> PKL[(books_w2v.pkl)]
    PKL --> CSV[books.csv]
  end

  CS --> A
  A --> S
  S --> U
