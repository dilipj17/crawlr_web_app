var infinite = new Waypoint.Infinite({
  element: $('.infinite-container')[0],
  onBeforePageLoad: function() {
    $('.loading').show();
  },
  onAfterPageLoad: function($items) {
    $('.loading').hide();
  }
});

function postQuestion(){
  var $ques = $('#add_question');
  $.ajax({
  type: "POST",
  url:$ques.data('url'),
  data: {
      'question':$ques.val(),
      'csrfmiddlewaretoken': $ques.data('csrf'),
    },
  success:function(res){
      responce = JSON.parse(res)
      if (responce.status == 200) {
        $('#mesaage').css('display', 'block');
        $('#mesaage').addClass('alert-info');
        $('#mesaage').html('your question successfully submited !');
      }
      else {
        $('#mesaage').css('display', 'block');
        $('#mesaage').addClass('alert-danger');
        $('#mesaage').html('Something went wrong please try again later');
      }
      location.reload(true);
    }
  });
  $('#closepopque').click()
}
