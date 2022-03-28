function colorize_input_valid(input){
	$(input).removeClass('is_invalid');
	$(input).addClass('is_valid');
	$(input).closest('.form-group').find('label').removeClass('is_invalid_label');
	$(input).closest('.form-group').find('label').addClass('is_valid_label');
}
function colorize_input_invalid(input){
	$(input).removeClass('is_valid');
	$(input).addClass('is_invalid');
	$(input).closest('.form-group').find('label').removeClass('is_valid_label');
	$(input).closest('.form-group').find('label').addClass('is_invalid_label');
}