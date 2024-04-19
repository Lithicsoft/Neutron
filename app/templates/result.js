window.onload = function() {
    var resultDiv = document.querySelector('.result');
    if (resultDiv && resultDiv.innerHTML.trim() === '') {
        resultDiv.style.display = 'none';
    } else if (resultDiv) {
        resultDiv.style.display = 'block';
    }
};
