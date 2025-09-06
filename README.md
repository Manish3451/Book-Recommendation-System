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


