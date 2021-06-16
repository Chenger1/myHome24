class BaseCloner {
	constructor(prefix, selector){
		this.prefix = prefix;
		this.selector = selector;
		this.newElement;
	}

	init(){
		// set base events for server-side rendered forms
		let local_setDeleteEvent = this.setDeleteEvent.bind(this);
		$('.delete_icon_'+this.prefix).each(function(){
			local_setDeleteEvent(this);
		})
		$(this.selector).each(function(){
			$(this).find('input[type=file]').on('change', function(){
            	setPreview(this);
        	});
		})
	}

	setDeleteEvent(element){
		let local_deleteRow = this.deleteRow.bind(this);
		let local_deleteRowWhoutReload = this.deleteRowWithoutReload.bind(this);
		if($(element).hasClass('has_pk')){ // if form has instance, we have to delete it from database
			$(element).on('click', function(){
				if(confirm('Вы точно хотите удалить этот блок?')){
					local_deleteRowWhoutReload(this);
				}
			})
		}else{ // otherwise just delete html block
			$(element).on('click', function(){
				if(confirm('Вы точно хотите удалить этот блок?')){
					local_deleteRow(this);
				}
			})
		}
	}

	clone(){
		// template
		this.cloneRow();
		this.setPreviewEvent();
		this.updateCounter(this.newElement, this.getCounterVal());
		this.setCallback();
		return true;
	}

	getCounterVal(){
		let total = $('#id_'+this.prefix+'-TOTAL_FORMS').val();
		let hidden_forms = $(this.selector+':hidden').not('#hidden_'+this.prefix);
		let counter_val = Number(total) - hidden_forms.length;
		return counter_val;
	}

	cloneRow(){
		let total = $('#id_'+this.prefix+'-TOTAL_FORMS').val();
		this.newElement = $('#hidden_'+this.prefix).clone(true).css('display', '').removeAttr('id');
		this.newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function(){ 
			// find all inputs which are no 'button, submit, reset'
			// replace the name and id of this inputs with new one to fit in to current forms row
			const name = $(this).attr('name').replace('__prefix__', total);
			const id = 'id_' + name;
			$(this).attr({'name': name, 'id': id}).val('').removeAttr('checked'); 
			// set new attributtes and remove 'checked' attr to create fresh form
		});
		let local_deleteRow = this.deleteRow.bind(this); // we have to bind method locally because of specifi behaviour of "this" keyword
		this.newElement.closest(this.selector).find('.delete_icon_'+this.prefix).on('click', function(){
    		local_deleteRow(this); // add "deleteRow" event to new forms
    	});

		total++;
		$('#id_'+this.prefix+'-TOTAL_FORMS').val(total); // increment and update TOTAL_FORMS input
		$(this.selector).last().after(this.newElement); // add newElement after last one
		return true;
	}

	deleteRow(element){
		const total = parseInt($('#id_'+this.prefix+'-TOTAL_FORMS').val());
		let parent_div = $(element).closest(this.selector); // find parent div
		parent_div.remove();
		$('#id_'+this.prefix+'-TOTAL_FORMS').attr('value', total-1); // update total 
		this.updateIndex(element); // update all formset sets according to new value in total
		this.deleteEvent();
	}

	hideRow(element){
		let parent_div = $(element).closest(this.selector);
		parent_div.find('input[type=checkbox][name*="-DELETE"]').prop('checked', true);
		parent_div.hide();
		// this.updateIndex(element);
		this.deleteEvent();
	}

	deleteRowWithoutReload(element){
		this.hideRow(element);
	}

	updateIndex(element){
		const forms = this.getForms(); // because of different html block structure we have to get forms specific to each case
		const local_prefix = this.prefix; // we have to bind method locally because of specifi behaviour of "this" keyword
		const id_regex = new RegExp('(' + this.prefix + '-\\d+)'); // set Regular Expression to find formset inputs
		let local_updateCounter = this.updateCounter.bind(this);
		let i;
		for(i=0; i<forms.length; i++){
			$(forms.get(i)).find(':input').each(function(){
				const replacement = local_prefix + '-' + i;
				// $(this).closest('div[class*=col]').find('.counter').text(i+1);
				local_updateCounter($(this), i+1);
				if($(this).attr('for')){ // check 'for' attr and replace it`s value to new one`
					$(this).attr('for', $(this).attr('for').replace(id_regex, replacement));
				};
				if(this.id){
					this.id = this.id.replace(id_regex, replacement); // replace id`s value`
				};
				if (this.name){
					this.name = this.name.replace(id_regex, replacement); // replace element`s name value
				};


			})
		}
	}

	getForms(){
		// get forms
		return $(this.selector).not('[id*=hidden_]');
	}

	setPreviewEvent(){};
	updateCounter(){};
	setCallback(event=undefined){};
	deleteEvent(){};
}


class AdvancedFormsetCloner extends BaseCloner{
	constructor(prefix, selector, url){
		super(prefix, selector, url); // call constructor from BaseCloner
	}

	setPreviewEvent(){ // set additional event for new formset
		this.newElement.find('input[type=file]').each(function(){
			$(this).on('change', function(){
				setPreview(this);
			})
		})
	}

	getForms(){
		// get all forms
		return $(this.selector).closest('.row').find(this.selector).not('div[id*=hidden_]').not(':hidden');
	}
}


class AdvancedFormsetClonerWithCounter extends AdvancedFormsetCloner{
	constructor(prefix, selector){
		super(prefix, selector);
	}

	updateCounter(element, value){
		$(element).closest('div[class*=col]').find('.counter').text(value);
	}
}



class FormsetClonerWithCallback extends BaseCloner{
	constructor(prefix, selector, event, delete_event){
		super(prefix, selector);
		this.event = event;
		this.delete_event = delete_event;
	}

	setCallback(){
		this.event(this.newElement, this.selector);
	}

	deleteEvent(){
		this.delete_event(this.newElement, this.selector);
	}
}