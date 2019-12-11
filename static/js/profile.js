$(document).ready(function() {
  var $data = $("#profileurl");
  $.ajax({
    type: "GET",
    url: $data.val(),
    success: function(res) {

      responce = JSON.parse(res);
      if (responce.status == 200) {
        $("#profileimage1").html(
          '<img  class="rounded-circle z-depth-2" src="' +
            responce.image +
            '" width="32" height="32"></img>'
        );
        $("#profileimage2").html(
          '<img  class="rounded-circle z-depth-2" src="' +
            responce.image +
            '" width="80" height="80"></img>'
        );
        $("#fullname1").html(responce.fullName);
        $("#fullname2").html(responce.fullName);
        $("#email").html(responce.email);
        $("#about").html(responce.bio);
        $("#searches").html(responce.searches);
        $("#questions").html(responce.questions);
        $("#replys").html(responce.karma);
      } else {
        console.log("some error occured");
      }
    }
  });
});
