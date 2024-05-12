function getSuggestions(query) {
    if (query.length > 0) {
        fetch('/api/search/suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({keyword: query})
        })
        .then(response => response.json())
        .then(data => {
            let suggestions = document.getElementById('suggestions');
            suggestions.innerHTML = '';
            suggestions.style.display = 'block';
            for (let i = 0; i < data.length; i++) {
                let div = document.createElement('div');
                div.innerHTML = data[i];
                div.className = 'suggestion';
                div.onclick = function() {
                    document.getElementById('search-input').value = this.innerHTML;
                    suggestions.style.display = 'none';
                };
                suggestions.appendChild(div);
            }
        });
    } else {
        document.getElementById('suggestions').style.display = 'none';
    }
}

function getspecialSuggestions(query) {
    if (query.length > 0) {
        fetch('/api/search/suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({keyword: query})
        })
        .then(response => response.json())
        .then(data => {
            let suggestions = document.getElementById('suggestionsspecial');
            suggestions.innerHTML = '';
            suggestions.style.display = 'block';
            for (let i = 0; i < data.length; i++) {
                let div = document.createElement('div');
                div.innerHTML = data[i];
                div.className = 'suggestion';
                div.onclick = function() {
                    document.getElementById('search-input').value = this.innerHTML;
                    suggestions.style.display = 'none';
                };
                suggestions.appendChild(div);
            }
        });
    } else {
        document.getElementById('suggestionsspecial').style.display = 'none';
    }
}