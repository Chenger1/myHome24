    function update_owner_info(data){
        if(!jQuery.isEmptyObject(data)){
            $('#owner').text(data['full_name']);
            $('#phone').text(data['phone']);
        }else{
            $('#owner').text('Не выбран');
            $('#phone').text('Не выбран');
        }
    }