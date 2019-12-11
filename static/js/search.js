var $timer = setInterval(function() {
  var $id = $('input[name=id]').val()
  var $url = $('input[name=result_url]').val()
  var $data = $('#data')
  $data.html('<div class="loading" style="display: block;text-align:center"><lottie-player src="https://assets3.lottiefiles.com/datafiles/fPx4vaZrul2Fvg9/data.json" mode="normal" speed="1" style="width:150px; height: 150px;" hover loop autoplay></lottie-player></div>')
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
        if (responce.status == "D") {
          $data.html(JSON.stringify(responce.result))
          clearTimeout($timer)
        }
        if (responce.status == "ERR") {
          $data.html('server error occured')
          clearTimeout($timer)
        }
      }
    }
  });
}, 2500);
