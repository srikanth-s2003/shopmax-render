document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    const suggestionsBox = document.createElement('div');
    suggestionsBox.className = 'suggestions-box';
    searchInput.parentNode.appendChild(suggestionsBox);

    // Cache for storing previous search results
    const searchCache = new Map();
    let debounceTimer;
    let currentFocus = -1;

    function displaySuggestions(suggestions) {
        suggestionsBox.innerHTML = '';
        
        if (suggestions.length > 0) {
            suggestions.forEach((suggestion, index) => {
                const div = document.createElement('div');
                div.className = 'suggestion-item';
                div.textContent = suggestion;
                div.setAttribute('data-index', index);
                
                // Highlight the matching text
                const searchTerm = searchInput.value.toLowerCase();
                const suggestionText = suggestion.toLowerCase();
                const startIndex = suggestionText.indexOf(searchTerm);
                
                if (startIndex !== -1) {
                    const beforeMatch = suggestion.slice(0, startIndex);
                    const match = suggestion.slice(startIndex, startIndex + searchTerm.length);
                    const afterMatch = suggestion.slice(startIndex + searchTerm.length);
                    div.innerHTML = `${beforeMatch}<strong>${match}</strong>${afterMatch}`;
                }
                
                div.addEventListener('click', () => {
                    searchInput.value = suggestion;
                    suggestionsBox.style.display = 'none';
                    searchInput.form.submit();
                });
                
                suggestionsBox.appendChild(div);
            });
            suggestionsBox.style.display = 'block';
        } else {
            suggestionsBox.style.display = 'none';
        }
    }

    function handleArrowKeys(e) {
        const items = suggestionsBox.getElementsByClassName('suggestion-item');
        
        if (items.length === 0) return;

        // Remove previous active class
        if (currentFocus >= 0 && items[currentFocus]) {
            items[currentFocus].classList.remove('active');
        }

        // Arrow Up
        if (e.key === 'ArrowUp') {
            e.preventDefault();
            currentFocus = currentFocus <= 0 ? items.length - 1 : currentFocus - 1;
        }
        // Arrow Down
        else if (e.key === 'ArrowDown') {
            e.preventDefault();
            currentFocus = currentFocus >= items.length - 1 ? 0 : currentFocus + 1;
        }
        // Enter
        else if (e.key === 'Enter' && currentFocus > -1) {
            e.preventDefault();
            if (items[currentFocus]) {
                searchInput.value = items[currentFocus].textContent;
                suggestionsBox.style.display = 'none';
                searchInput.form.submit();
            }
        }

        // Add active class to current item
        if (items[currentFocus]) {
            items[currentFocus].classList.add('active');
            // Scroll item into view if needed
            items[currentFocus].scrollIntoView({ block: 'nearest' });
        }
    }

    searchInput.addEventListener('input', function(e) {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim().toLowerCase();
        
        if (query.length === 0) {
            suggestionsBox.style.display = 'none';
            return;
        }

        // Check cache first
        if (searchCache.has(query)) {
            displaySuggestions(searchCache.get(query));
            return;
        }

        // Only make request if query is 2 or more characters
        if (query.length >= 2) {
            debounceTimer = setTimeout(() => {
                fetch(`/search/ajax/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.suggestions) {
                        // Cache the results
                        searchCache.set(query, data.suggestions);
                        // Only display if the input value hasn't changed
                        if (searchInput.value.trim().toLowerCase() === query) {
                            displaySuggestions(data.suggestions);
                        }
                    }
                });
            }, 300);
        }
    });

    searchInput.addEventListener('keydown', handleArrowKeys);

    // Close suggestions when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = 'none';
            currentFocus = -1;
        }
    });

    // Clear cache periodically to prevent memory bloat
    setInterval(() => {
        searchCache.clear();
    }, 5 * 60 * 1000); // Clear cache every 5 minutes
}); 