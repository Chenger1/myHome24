function saveMeter(url){
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
				renderNewMeter(context);
			}
		}
	})
}

function renderNewMeter(response){

}