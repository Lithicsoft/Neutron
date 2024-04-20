window.onload = function() {
  var url = new URL(window.location.href);

  function setBorderBottom(id, value) {
    document.getElementById(id).style.borderBottom = value;
  }

  function removeDisplay(id) {
    var element = document.getElementById(id);
    if (element) {
      element.remove();
    }
  }

  var CurrentType = url.searchParams.get('tp');
  if (CurrentType == null) {
    setBorderBottom("TextTag", "0.2em solid rgb(23, 74, 228)");
    removeDisplay("image_display");
    removeDisplay("video_display");
  } else if (CurrentType == "Text") {
    setBorderBottom("TextTag", "0.2em solid rgb(23, 74, 228)");
    removeDisplay("image_display");
    removeDisplay("video_display");
  } else if (CurrentType == 'Image') {
    setBorderBottom("ImgTag", "0.2em solid rgb(23, 74, 228)");
    removeDisplay("text_display");
    removeDisplay("video_display");
  } else if (CurrentType == 'Video') {
    setBorderBottom("VidTag", "0.2em solid rgb(23, 74, 228)");
    removeDisplay("text_display");
    removeDisplay("image_display");
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
}

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

var timeSelect = document.querySelector('#timeSelect');

var params = new URLSearchParams(window.location.search);
var hl = params.get('tm');
if (hl) {
  timeSelect.value = hl;
}

timeSelect.addEventListener('change', function() {
  var tm = this.options[this.selectedIndex].getAttribute('result-time');
  
  if (tm == 'all') {
    params.delete('tm');
    window.history.replaceState({}, '', '?' + params.toString());
  } else {
    params.set('tm', tm);
    window.history.replaceState({}, '', '?' + params.toString());
  }

  window.location.reload();
});

function changePage(pageNumber) {
  if (!isNaN(pageNumber)) {
    var url = new URL(window.location.href);
    url.searchParams.set('pg', pageNumber);
    window.history.pushState({}, '', url.toString());
    window.location.reload();
  }
}

function showFilter() {
  var x = document.getElementById("Dropdown");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}