window.onload = function() {
    var resultDiv = document.querySelector('.result');
    if (resultDiv && resultDiv.innerHTML.trim() === '') {
        resultDiv.style.display = 'none';
    } else if (resultDiv) {
        resultDiv.style.display = 'block';
    }

    var wikipediaDiv = document.querySelector('.wikipedia');
    if (wikipediaDiv) {
        var titleElement = wikipediaDiv.querySelector('h3');
        if (titleElement && titleElement.innerHTML.trim() === '') {
            wikipediaDiv.style.display = 'none';
        } else {
            wikipediaDiv.style.display = 'block';
        }
    }
};
