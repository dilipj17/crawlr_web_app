$(document).ready(function() {
  var $data = $("#profileurl");
  console.log($data.val());

  $.ajax({
    type: "GET",
    url: $data.val(),
    success: function(res) {
      console.log(res);

      responce = JSON.parse(res);
      if (responce.status == 200) {
        // write responce to give location
        $("#profile-data").html(responce.fullName);
      } else {
        console.log("some error occured");
      }
    }
  });
});
