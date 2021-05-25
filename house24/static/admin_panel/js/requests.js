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


function send_request_to_get_house_info(element, url){
    let value = $(element).find(':selected').val();
    let sections = $('#section');
    let floors = $('#floor');
    $.ajax({
      url: url,
      type: 'GET',
      data: {'pk': value},
    })
    .done(function(response) {
      sections.children().remove();
      floors.children().remove();
      sections.append('<option disabled selected>---------</option>');
      floors.append('<option disabled selected>---------</option>');
      for(key in response['sections']){
        append_select_option(sections, response['sections'][key]);
      }
      for(key in response['floors']){
        append_select_option(floors, response['floors'][key]);
      }

    })
}

function append_select_option(selector, data){
    $(selector).append('<option value='+ data['pk'] +' >' + data['name'] + '</option>')
}