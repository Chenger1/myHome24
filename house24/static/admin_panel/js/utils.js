    function update_owner_info(data){
        if(!jQuery.isEmptyObject(data)){
            $('#owner').text(data['full_name']);
            $('#phone').text(data['phone']);
        }else{
            $('#owner').text('Не выбран');
            $('#phone').text('Не выбран');
        }
    }

    function submit_form_after_keypress(){
        $('.form-control').each(function(){
            $(this).keydown(function(event) {
                if(event.which == 13){
                    $('form').submit();
                }
            });
       })
        $('.select2-selection').each(function(){
            $(this).on('keyup', function(e){
                if(e.keyCode === 13){
                    $('form').submit();
                }
            })
        })
    }

function submit_form_after_ordering(){
    $('.submit_link').each(function(){
        $(this).on('click', function(e){
            e.preventDefault();
            const link =$(this).closest('th').find('.next_link').val();
            $('form').prop('action', link).submit();
        })
    })
}

function confirm_deleting(){
    $('.delete_instances').each(function(){
        $(this).on('click', function(e){
            if(!confirm('Вы уверен что хотите удалить эту запись?')){
                e.preventDefault();
            }
        })
    })
}