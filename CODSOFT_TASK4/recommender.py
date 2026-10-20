"""
Content-Based Recommendation Engine using TF-IDF Vectorization and Cosine Similarity.
"""

from typing import List, Dict, Any
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from data_loader import load_movie_data

class MovieRecommender:
    def __init__(self) -> None:
        self.df = load_movie_data()
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self._build_model()

    def _build_model(self) -> None:
        """Computes TF-IDF vector matrix and pairwise cosine similarity matrix."""
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df['combined_features'])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def get_movie_titles(self) -> List[str]:
        """Returns list of all searchable movie titles."""
        return self.df['title'].tolist()

    def recommend(self, title: str, top_n: int = 5) -> List[Dict[str, Any]]:
        """
        Calculates and returns top N recommended movies similar to input title.
        Supports substring and case-insensitive matching.
        """
        matching_indices = self.df[self.df['title'].str.lower() == title.lower()].index
        if len(matching_indices) == 0:
            matching_indices = self.df[self.df['title'].str.lower().str.contains(title.lower(), regex=False)].index

        if len(matching_indices) == 0:
            return []

        idx = matching_indices[0]
        similarity_scores = list(enumerate(self.similarity_matrix[idx]))
        
        # Sort by highest similarity score
        sorted_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Exclude self-match (index 0 in sorted list)
        recommendations = []
        for score_idx, score in sorted_scores[1:top_n + 1]:
            movie_row = self.df.iloc[score_idx]
            recommendations.append({
                'movieId': int(movie_row['movieId']),
                'title': str(movie_row['title']),
                'genres': str(movie_row['genres']).replace('|', ', '),
                'similarity_score': round(float(score), 4)
            })

        return recommendations