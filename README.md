Book Recommendation System

This project implements a book recommendation system that suggests books to users based on their preferences. The system leverages natural language processing (NLP) techniques, specifically Word2Vec, to understand book similarities and provide relevant recommendations.

Table of Contents

Features

System Architecture

Technologies Used

Setup and Installation

Usage

Project Structure

Contributing

License

Contact

Features

Content-Based Recommendations: Recommends books similar to a given input book based on their descriptions and genres.

Intuitive Web Interface: A user-friendly interface built with Streamlit for easy interaction.

Scalable API: A FastAPI backend to serve recommendation requests efficiently.

Word2Vec Embeddings: Utilizes Word2Vec to generate dense vector representations of books, capturing semantic meanings.

Cosine Similarity: Employs cosine similarity to calculate the similarity between book embeddings.

System Architecture

The system is designed with a layered architecture to ensure modularity, scalability, and maintainability.

code
Mermaid
download
content_copy
expand_less

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

1. Frontend Layer (Streamlit Web App):
* Provides the user interface for interacting with the recommendation system.
* Allows users to input a book title and view recommendations.
* Communicates with the FastAPI backend to fetch recommendations.

2. API Layer (FastAPI API Server):
* Acts as an intermediary between the frontend and the machine learning model.
* Exposes a /recommend endpoint that accepts a book title.
* Handles incoming requests, processes them, and returns recommendations.

3. ML Model Layer (Word2Vec & Cosine Similarity):
* Word2Vec Model: Pre-trained or trained on book descriptions to generate vector embeddings for words.
* Book Embeddings: Each book is represented as a vector, typically an aggregation of its word embeddings.
* Cosine Similarity: Calculates the similarity between the input book's embedding and all other book embeddings to find the most similar books.

4. Data Layer (Persistent Storage):
* books.csv: Contains the raw book data, including titles, descriptions, and other relevant information.
* books_w2v.pkl: Stores the pre-calculated Word2Vec embeddings for all books, allowing for faster retrieval during recommendation generation.

Technologies Used

Python: The primary programming language.

Streamlit: For building the interactive web user interface.

FastAPI: For creating the RESTful API server.

Gensim: For implementing and managing the Word2Vec model.

Pandas: For data manipulation and analysis.

Scikit-learn: For machine learning utilities, specifically cosine similarity.

Uvicorn: ASGI server to run FastAPI.

Setup and Installation

Follow these steps to set up and run the Book Recommendation System locally:

1. Clone the Repository
code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
git clone https://github.com/Manish3451/Book-Recommendation-System.git
cd Book-Recommendation-System
2. Create a Virtual Environment (Recommended)
code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install Dependencies
code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
pip install -r requirements.txt
4. Data Preparation and Model Training (if not already done)

Ensure you have the books.csv file in your project root. If books_w2v.pkl is not present or you want to retrain the model, you might need to run a script to generate the embeddings.

(Assuming you have a script like train_model.py or prepare_data.py to generate books_w2v.pkl)

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
python src/train_model.py # Or whatever your model training script is named
Usage
1. Run the FastAPI Backend

Navigate to the project root and start the FastAPI server:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

The API will be accessible at http://localhost:8000. You can test the /recommend endpoint (e.g., http://localhost:8000/recommend?book_title=The Hitchhiker's Guide to the Galaxy).

2. Run the Streamlit Frontend

Open a new terminal, activate your virtual environment, and run the Streamlit app:

code
Bash
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
streamlit run src/app.py

This will open the Streamlit web application in your browser, typically at http://localhost:8501.

Project Structure
code
Code
download
content_copy
expand_less
IGNORE_WHEN_COPYING_START
IGNORE_WHEN_COPYING_END
Book-Recommendation-System/
├── data/
│   └── books.csv                 # Raw dataset of books
├── models/
│   └── books_w2v.pkl             # Pre-trained Word2Vec embeddings for books
├── src/
│   ├── api.py                    # FastAPI application for the recommendation API
│   ├── app.py                    # Streamlit web application
│   ├── model.py                  # Contains the recommendation logic (Word2Vec, Cosine Similarity)
│   └── utils.py                  # Utility functions (e.g., data loading, preprocessing)
├── requirements.txt            # Python dependencies
├── README.md                   # This README file
└── .gitignore                  # Files and directories to ignore in Git
Contributing

Contributions are welcome! If you have any suggestions, bug reports, or want to add new features, please feel free to:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature-name).

Make your changes.

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/your-feature-name).

Open a Pull Request.

License

This project is licensed under the MIT License - see the LICENSE file for details. (Note: You might need to create a LICENSE file if it doesn't exist)

Contact

If you have any questions or feedback, please feel free to reach out:

Manish - [Your Email/LinkedIn/GitHub Profile]

Note: This README assumes a standard structure for your Python project. You might need to adjust file paths and script names (e.g., src/train_model.py) based on your actual project implementation. Make sure to replace placeholders like [Your Email/LinkedIn/GitHub Profile] with your actual information.

