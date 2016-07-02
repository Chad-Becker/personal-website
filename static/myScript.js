$(document).ready(function(){

// ---------------------Smooth Scrolling----------------------------------

  // Add smooth scrolling to all links in navbar, text, and footer link
  $(".scroll").on("click", function(event) {
    event.preventDefault();

    var hash = this.hash;

    $("html, body").animate({
     scrollTop: $(hash).offset().top
   }, 1000, function(){

    window.location.hash = hash;
  });
  });

// ---------------------Popovers------------------------------------------

$("[data-toggle='popover']").popover();

// ---------------------Slide-In Animation--------------------------------

if($(window).width() < 1680) {
  $(window).scroll(function() {
    $(".slideanim").each(function(){
      var pos = $(this).offset().top - 700;

      var winTop = $(window).scrollTop();
      if (pos < winTop) {
        $(this).addClass("slide");
      }
    });
  });
}

else {
  $(window).scroll(function() {
    $(".slideanim").each(function(){
      var pos = $(this).offset().top - 1000;

      var winTop = $(window).scrollTop();
      if (pos < winTop) {
        $(this).addClass("slide");
      }
    });
  });
}

// ---------------------Sending Client Time Offset-------------------------

$("#visitorsLog .btn").click(function() {
  var now = new Date();
  var clientOffset = now.getTimezoneOffset();

  $.post("/clientTimeOffset", {
    clientOffset: clientOffset
  }, "json");
});

});