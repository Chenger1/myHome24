function cloneRow(prefix, selector){
    let total = $('#id_'+prefix+'-TOTAL_FORMS').val();;

    let newElement = $('#hidden_'+prefix).clone(true).css('display', '').removeAttr('id');

    newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function(){ 
	// find all inputs which are no 'button, submit, reset'
	// replace the name and id of this inputs with new one to fit in to current forms row
		var name = $(this).attr('name').replace('__prefix__', total);
		let id = 'id_' + name;
		$(this).attr({'name': name, 'id': id}).val('').removeAttr('checked'); 
		// set new attributtes and remove 'checked' attr to create fresh form
	});

    $(newElement).closest(selector).find('.delete_icon_'+prefix).on('click', function(){
    	deleteRow(this, prefix, selector);
    })

    newElement.find('input[type=file]').each(function(){
    	$(this).on('change', function(){
    		setPreview(this);
    	})
    })

	total++;
	$('#id_'+prefix+'-TOTAL_FORMS').val(total); // increment and update TOTAL_FORMS input
	$(newElement).closest('div[class*=col]').find('.counter').text(total);
	$(selector).last().after(newElement); // add newElement after last one
	return false;

}

function updateIndex(element, prefix, selector){
	let forms = $(selector).closest('.row').find(selector).not('div[id*=hidden_]')

	for(i=0; i<forms.length; i++){
		$(forms.get(i)).find(':input').each(function(){
				let id_regex = new RegExp('(' + prefix + '-\\d+)'); // set Regular Expression to find formset inputs
				let replacement = prefix + '-' + i;
				$(this).closest('div[class*=col]').find('.counter').text(i+1);
				if($(this).attr('for')){ // check 'for' attr and replace it`s value to new one`
					$(this).attr('for', $(this).attr('for').replace(id_regex, replacement));
				}
				if(this.id){
					this.id = this.id.replace(id_regex, replacement); // replace id`s value`
				}
				if (this.name){
					this.name = this.name.replace(id_regex, replacement); // replace element`s name value
				}
		})
	}
}


function deleteRow(element, prefix, selector){
	var total = parseInt($('#id_'+prefix+'-TOTAL_FORMS').val())
	// parent_div = $(element).closest('div[class*=col]')
	parent_div = $(element).closest(selector);

	parent_div.remove();
	$('#id_'+prefix+'-TOTAL_FORMS').attr('value', total-1);

	updateIndex(element, prefix, selector)

}

function deleteFormsetWithoutReload(element, url, prefix, selector){
	pk = $(element).attr('name')
	$.ajax({
		method: 'GET',
		url: url,
		data: {'pk': pk},
		success: function(response){
			deleteRow(element, prefix, selector);
		}
	})
}