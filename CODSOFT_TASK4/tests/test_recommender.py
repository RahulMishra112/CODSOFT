"""
Automated Test Suite for Movie Recommendation System.
Updated for Indian Cinema & Global Masterpieces collection.
"""

import pytest
from recommender import MovieRecommender

@pytest.fixture
def recommender():
    return MovieRecommender()

def test_dataset_loading(recommender):
    """Verifies that the dataset loads a non-empty list of titles."""
    titles = recommender.get_movie_titles()
    assert len(titles) > 0

def test_valid_recommendations(recommender):
    """Verifies that recommending for a valid movie returns results and excludes self-match."""
    results = recommender.recommend("RRR", top_n=3)
    assert len(results) == 3
    
    # Selected movie must NOT recommend itself
    recommended_titles = [r['title'] for r in results]
    assert "RRR (2022)" not in recommended_titles

def test_invalid_movie_title(recommender):
    """Verifies that unknown movie titles safely return an empty result list."""
    results = recommender.recommend("Non Existent Movie Title 12345", top_n=5)
    assert len(results) == 0

def test_top_n_constraint(recommender):
    """Verifies that requested recommendation count (top_n) is strictly respected."""
    results = recommender.recommend("Baahubali", top_n=2)
    assert len(results) == 2