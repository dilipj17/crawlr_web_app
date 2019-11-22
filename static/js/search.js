var $timer = setInterval(function() {
  var $id = $('input[name=id]').val()
  var $url = $('input[name=result_url]').val()
  var $data = $('#data')
  $data.html('loading ... ')
  $.ajax({
    type: 'GET',
    url: $url,
    data: {
      'id': $id
    },
    success: function(res, code) {
      responce = JSON.parse(res)
      if (responce['code']) {
        if (responce['code'] == 400) {
          $data.html('something went wrong try again later')
          clearTimeout($timer)
        }
        if (responce['code']== 401) {
          $data.html('you are not authorized to see this results')
          clearTimeout($timer)
        }
      }
      else {
        $data.html(responce)
      }
    }
  });
}, 2500);
