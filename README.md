# 📚 Book Recommendation System

A content-based **Book Recommendation System** built with **Word2Vec embeddings** on book descriptions.  
It provides a **FastAPI backend** and a **Streamlit frontend**, both containerized for deployment on [Render](https://render.com).

---

## 🏗️ System Architecture

```mermaid
flowchart LR
    subgraph UI["🎨 Streamlit UI"]
        U[User] --> S[Streamlit Frontend]
    end

    subgraph API["⚡ FastAPI Backend"]
        S --> A[/Recommend Endpoint/]
    end

    subgraph Model["🧠 Recommender Core"]
        A --> W2V[Word2Vec Model + Embeddings]
        W2V --> DB[(books_w2v.pkl)]
    end

    subgraph Storage["🗂️ Data"]
        DB -.-> CSV[books.csv]
    end
Book-Recommendation-System/
├── app/
│   └── api.py                 # FastAPI backend
├── data/
│   ├── books.csv              # Raw data (input)
│   └── books_w2v.pkl          # Trained model artifact
├── scripts/
│   └── build_tfidf_and_save.py # Script to train and save Word2Vec model
├── streamlit_app.py           # Streamlit UI
├── requirements.txt           # Python dependencies
├── Dockerfile.api             # Dockerfile for FastAPI
├── Dockerfile.ui              # Dockerfile for Streamlit
├── render.yaml                # Render deployment blueprint
├── .gitignore
└── README.md

---

✅ With this change:
- The **architecture diagram** will render correctly (Mermaid).  
- The **folder structure** will show as plain code block (no Mermaid parsing).  

---

Do you also want me to add a **sequence diagram** (Mermaid) for the full request flow (User → Streamlit → FastAPI → Model → Response) in the README? That way you’ll have both an **architecture diagram** and a **flow diagram**.
