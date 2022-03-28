function setCheckbox(element){
	if($(element).prop('checked')){
		changeCheckboxesStatus(true);
	}else{
		changeCheckboxesStatus(false);
	}
}

function changeCheckboxesStatus(status){
	$('.delete_checkbox').each(function(){
		$(this).prop('checked', status);
	})
}