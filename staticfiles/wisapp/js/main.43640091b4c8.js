let burger = document.querySelector('.burger');
let modalWindiow = document.querySelector('.mobile__modal')


burger.addEventListener('click', function() {
    modalWindiow.classList.toggle('active');
    burger.classList.toggle('active');
});



function openCity(evt, cityName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(cityName).style.display = "block";
    evt.currentTarget.className += " active";
  };




  $(document).on('ready', function() {
    var checkboxes = $("input[type=checkbox]");
  
    $("#form").on('submit', function(e) {
      var checker = false;
      checkboxes.each(function() {
        if ($(this).prop('checked') == true) {
          checker = true;
        }
      });
  
      if (checker == false) {
        e.preventDefault();
        alert('не выбран ни один чекбокс, форма не отправлена');
      } else {
        alert('выбран хотя бы 1 чекбокс, форма отправлена');
      }
    });
  });
