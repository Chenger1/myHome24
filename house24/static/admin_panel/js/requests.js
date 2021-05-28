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

function update_select(element, url, parent_pk){
    $.ajax({
        url: url,
        type: 'GET',
        data: {'pk': parent_pk},
    })
    .done(function(response){
        $(element).children().remove();
        for(key in response){
            append_select_option(element, response[key]);
        }
    })
}


function append_select_option(selector, data){
    $(selector).append('<option value='+ data['id'] +' >' + data['name'] + '</option>')
}