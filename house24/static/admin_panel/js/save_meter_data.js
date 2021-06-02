function saveMeter(url){
	const date = $('#created').val();
	const house = $('#house').find(':selected').val();
	const section = $('#section').find(':selected').val();
	const flat = $('#flat').find(':selected').val();
	if(!flat){
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
		data[selected.text()] = {
			'pk': selected.val(),
			'outcome': outcome.val(),
		}
	}

	$.ajax({
		method: 'GET',
		url: url,
		data: {'date': date,
			   'house': house,
			   'section': section,
				'flat': flat,
				'data': data},
		success: function(response){
			console.log(response);
		}
	})
}