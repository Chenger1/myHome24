function send_request(url, pk, select_measure){
	$.ajax({
		url: url,
        type: 'GET',
        data: {'pk': pk},
            })
    .done(function(response) {
        $(select_measure).children().remove();
        $(select_measure).append('<option>'+ response['measure_name'] +'</option>')
     })
}

function send_request_to_api(url, pk, callback){
    $.ajax({
        url: url,
        type: 'GET',
        data: {'pk': pk},
        success: function(response){
            callback(response);    
        }
    })
}

function update_select(element, url, parent_pk, constructor){
    $.ajax({
        url: url,
        type: 'GET',
        data: {'pk': parent_pk},
    })
    .done(function(response){
        $(element).children().remove();
        $(element).append('<option value>Выберите...</option>')
        for(key of response){
            constructor(element, key);
        }
    })
}


function append_select_section_floor(selector, data){
    $(selector).append('<option value='+ data['id'] +' >' + data['name'] + '</option>');
}
function append_select_flat(selector, data){
    $(selector).append('<option value="'+ data['id'] +'"> Кв. '+ data['number'] +'</options>');
}
