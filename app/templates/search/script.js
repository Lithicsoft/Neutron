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