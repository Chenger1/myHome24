function saveMeter(url, callback_url, flat_pk){
	let context = {};
	context['date'] = $('#created').val();
	context['house'] = $('#house').find(':selected').val();
	context['section'] = $('#section').find(':selected').val();
	context['flat'] = $('#flat').find(':selected').val();
	if(!context['flat']){
		confirm('Выберите квартиру чтобы сохранить новые показания!');
		return false;
	}
	const forms = $('.formset').not('#hidden_services');
	if(forms.length <=0){
		confirm('Добавьте услуги и расход чтобы сохранить новые показания!');
		return false;
	}
	let data = {};

	for(form of forms){
		let current_form = $(form);
		let selected = current_form.find(':selected');
		let outcome = current_form.find('.outcome');
		if(!outcome.val()){
			confirm('Добавьте расход для: "'+ selected.text() +'", чтобы сохранить новые показания!');
			return false;
		}
		data[selected.val()] = outcome.val();
	}
	context['data'] = data;

	$.ajax({
		method: 'GET',
		url: url,
		data: {'data':JSON.stringify(context)},
		success: function(response){
			if(response['status'] == 200){
				updateMeterTable(callback_url, flat_pk);
			}
		}
	})
}

function updateMeterTable(url, flat_pk=undefined){
	$.ajax({
		method: 'GET',
		url: url,
		data: {'pk': flat_pk},
		success: function(response){
			renderNewMeter(response);
		}
	})
}

function renderNewMeter(response){
	$('#meters_table > tbody').empty();
	let table =  $('#meters_table');
	for(index in response){
		let tr = $('<tr />');
		tr.append($('<td />', {text: response[index]['number']}));
		tr.append($('<td />', {html: getStatusWidget(response[index]['status'])}))
		tr.append($('<td />', {text: response[index]['date']}));
		tr.append($('<td />', {text: response[index]['month']}));
		tr.append($('<td />', {text: response[index]['house']}));
		tr.append($('<td />', {text: response[index]['section']}));
		tr.append($('<td />', {text: response[index]['flat']}));
		tr.append($('<td />', {text: response[index]['service']}));
		tr.append($('<td />', {text: response[index]['data']}));
		tr.append($('<td />', {text: response[index]['measure']}));
		table.append(tr);
	}
}

function getStatusWidget(status){
	if(status == 0){
		return '<small class="label label-warning">Новое</small>';
	}else if(status == 1){
		return '<small class="label label-success">Учтено</small>';
	}else if(status == 2){
		return '<small class="label label-success">Учтено и оплачено</small>';
	}else{
		return '<small class="label label-primary">Нулевое</small>';
	}
}