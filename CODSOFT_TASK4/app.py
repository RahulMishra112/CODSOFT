"""
Flask Web Application Server for AI Recommendation System.
"""

from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender

app = Flask(__name__)
recommender = MovieRecommender()

@app.route('/')
def home():
    """Renders main recommendation interface."""
    return render_template('index.html')

@app.route('/api/titles', methods=['GET'])
def get_titles():
    """Returns available movie titles for search autocompletion."""
    titles = recommender.get_movie_titles()
    return jsonify({'titles': titles})

@app.route('/api/recommend', methods=['POST'])
def recommend():
    """API Endpoint: Computes top recommendations for chosen movie."""
    data = request.get_json()
    title = data.get('title', '')
    top_n = int(data.get('top_n', 5))

    if not title:
        return jsonify({'error': 'Please provide a valid movie title'}), 400

    results = recommender.recommend(title=title, top_n=top_n)
    if not results:
        return jsonify({'error': f'Movie "{title}" not found in database.'}), 404

    return jsonify({
        'query_title': title,
        'count': len(results),
        'recommendations': results
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)