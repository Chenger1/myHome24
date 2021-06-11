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
