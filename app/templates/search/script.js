var tags = document.querySelectorAll('.tag');

tags.forEach(function(tag) {
  tag.addEventListener('click', function() {
    var type = this.getAttribute('data-type');
    
    var params = new URLSearchParams(window.location.search);
    
    params.set('type', type);
    
    window.history.replaceState({}, '', '?' + params.toString());

    window.location.reload();
  });
});

window.onload = function() {
  var resultDiv = document.querySelector('.result');
  if (resultDiv.innerHTML.trim() === '') {
      resultDiv.style.display = 'none';
  } else {
      resultDiv.style.display = 'block';
  }
};