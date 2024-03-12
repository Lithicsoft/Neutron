window.onload = function() {
    var resultDiv = document.querySelector('.result');
    if (resultDiv.innerHTML.trim() === '') {
        resultDiv.style.display = 'none';
    } else {
        resultDiv.style.display = 'block';
    }

    var wikipediaDiv = document.querySelector('.wikipedia');
    if (wikipediaDiv.innerHTML.trim() === '') {
        wikipediaDiv.style.display = 'none';
    } else {
        wikipediaDiv.style.display = 'block';
    }
};