document.addEventListener('DOMContentLoaded', () => {
    const movieInput = document.getElementById('movie-input');
    const autocompleteList = document.getElementById('autocomplete-list');
    const topNSelect = document.getElementById('top-n');
    const recommendBtn = document.getElementById('recommend-btn');
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    const loader = document.getElementById('loader');
    const errorMessage = document.getElementById('error-message');

    let availableTitles = [];

    // 1. Fetch search titles from Flask API
    fetch('/api/titles')
        .then(res => res.json())
        .then(data => {
            availableTitles = data.titles || [];
        })
        .catch(() => console.error("Could not fetch titles."));

    // 2. Real-time Autocomplete Filter
    movieInput.addEventListener('input', () => {
        const query = movieInput.value.toLowerCase().trim();
        autocompleteList.innerHTML = '';

        if (!query) {
            autocompleteList.classList.add('hidden');
            return;
        }

        const filtered = availableTitles.filter(t => t.toLowerCase().includes(query)).slice(0, 8);

        if (filtered.length > 0) {
            filtered.forEach(title => {
                const item = document.createElement('div');
                item.className = 'autocomplete-item';
                item.textContent = title;
                item.addEventListener('click', () => {
                    movieInput.value = title;
                    autocompleteList.classList.add('hidden');
                });
                autocompleteList.appendChild(item);
            });
            autocompleteList.classList.remove('hidden');
        } else {
            autocompleteList.classList.add('hidden');
        }
    });

    // Close autocomplete when clicking outside
    document.addEventListener('click', (e) => {
        if (e.target !== movieInput) autocompleteList.classList.add('hidden');
    });

    // 3. Trigger AI Recommendation
    recommendBtn.addEventListener('click', () => {
        const title = movieInput.value.trim();
        const topN = topNSelect.value;

        if (!title) {
            showError("Please enter or select a movie title.");
            return;
        }

        hideError();
        resultsSection.classList.add('hidden');
        loader.classList.remove('hidden');

        fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: title, top_n: topN })
        })
        .then(res => res.json())
        .then(data => {
            loader.classList.add('hidden');
            if (data.error) {
                showError(data.error);
                return;
            }
            renderResults(data.recommendations);
        })
        .catch(() => {
            loader.classList.add('hidden');
            showError("An error occurred computing recommendations.");
        });
    });

    function renderResults(movies) {
        resultsGrid.innerHTML = '';
        movies.forEach(movie => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <div>
                    <div class="card-title">${movie.title}</div>
                    <div class="card-genres">Genres: ${movie.genres}</div>
                </div>
                <div class="match-badge">${(movie.similarity_score * 100).toFixed(1)}% Match</div>
            `;
            resultsGrid.appendChild(card);
        });
        resultsSection.classList.remove('hidden');
    }

    function showError(msg) {
        errorMessage.textContent = msg;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
    }
});