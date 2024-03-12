var tags = document.querySelectorAll('.tag');

tags.forEach(function(tag) {
  tag.addEventListener('click', function() {
    var type = this.getAttribute('data-type');
    
    var params = new URLSearchParams(window.location.search);
    
    params.set('tp', type);
    
    window.history.replaceState({}, '', '?' + params.toString());

    window.location.reload();
  });
});

var languageSelect = document.querySelector('#languageSelect');

var params = new URLSearchParams(window.location.search);
var hl = params.get('hl');
if (hl) {
  languageSelect.value = hl;
}

languageSelect.addEventListener('change', function() {
  var lang = this.options[this.selectedIndex].getAttribute('result-language');
  
  if (lang == 'all') {
    params.delete('hl');
    window.history.replaceState({}, '', '?' + params.toString());
  } else {
    params.set('hl', lang);
    window.history.replaceState({}, '', '?' + params.toString());
  }

  window.location.reload();
});