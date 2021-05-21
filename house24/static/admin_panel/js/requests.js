function send_request(url, pk, select_measure){
	$.ajax({
		url: url,
        type: 'GET',
        data: {'pk': pk},
            })
    .done(function(response) {
        console.log(response)
        $(select_measure).children().remove();
        $(select_measure).append('<option>'+ response['measure_name'] +'</option>')
     })
}