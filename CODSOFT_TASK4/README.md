```markdown
# Task 4: Content-Based AI Movie Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Scikit--Learn](https://img.shields.io/badge/Scikit--Learn-TF--IDF-orange)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green)
![Dataset](https://img.shields.io/badge/Dataset-Indian%20%26%20Global%20Cinema-red)

A content-based recommendation system that analyzes metadata across **1,000+ Indian (Bollywood, Tollywood, Kollywood, Mollywood) and Global blockbuster movies**. It computes feature vectors using **TF-IDF Vectorization** and evaluates similarity distances using **Cosine Similarity**.

---

## 📌 Project Overview
The system allows users to search or select any movie title (e.g., *RRR*, *Baahubali*, *3 Idiots*, *KGF*, *Pathaan*) and instantly receive mathematically matched recommendations based on narrative themes, genres, and storyline overviews.

### Key Features
* **TF-IDF Vectorization:** Converts movie metadata and textual summaries into high-dimensional feature vectors.
* **Cosine Similarity Distance:** Computes directional similarities between movie vectors to find exact thematic matches:
  $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\Vert{}A\Vert{} \Vert{}B\Vert{}}$$
* **Indian Cinema Collection:** Expanded dataset featuring over 1,000 curated Indian and global masterpieces.
* **Cyberpunk Glassmorphism UI:** Features real-time autocomplete search, match-percentage tags, and dynamic recommendation scaling.

---

## 📁 Project Structure

```text
CODSOFT_TASK4/
├── app.py                  # Flask Web Server & API Endpoints
├── recommender.py          # TF-IDF & Cosine Similarity Engine
├── data_loader.py          # Movie Dataset Generator & Preprocessor
├── requirements.txt        # Project Dependencies
├── README.md               # Documentation
├── .gitignore              # Git Ignore Rules
├── data/
│   └── movies.csv          # Cached Dataset
├── templates/
│   └── index.html          # Cyberpunk Frontend UI
├── static/
│   ├── css/
│   │   └── style.css       # High-End Cyberpunk Glassmorphism
│   └── js/
│       └── app.js          # Autocomplete Search & Async API Handling
└── tests/
    └── test_recommender.py # Automated Test Suite




    🛠️ Technology Stack
Language: Python 3.10+

Machine Learning: Scikit-Learn (TfidfVectorizer, cosine_similarity), Pandas, NumPy

Backend Framework: Flask

Frontend: HTML5, CSS3, Vanilla JavaScript (ES6)

Testing: Pytest

🚀 Installation & Setup




Install Dependencies:

Bash
pip install -r requirements.txt
Run Unit Tests:

Bash
python -m pytest
Start Application Server:

Bash
python app.py
Open http://127.0.0.1:5000 in your web browser.

📊 Learning Outcomes
Applied Natural Language Processing (NLP) pre-processing techniques on unstructured movie text.

Constructed linear algebra vector spaces for content recommendation.

Implemented fuzzy autocomplete string matching in web applications.

👤 Author
Name: Rahul

Internship: CodSoft AI Internship (Task 4)