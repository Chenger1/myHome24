function ChatResponseManager(config, socket, append_message_func, url_path){
    this.appendMessage = function(name, img, side, text){
        append_message_func(name, img, side, text);
    }

    this.addNotificationMessage = function(data){
        append_message_func(data, url_path);
    }

    this.addRegularMessage = function(data){
        const msgText = data['text'];
        if(data['from_user'] === config['from_user_uuid']){
            this.appendMessage(config['from_user_name'], config['from_user_img'], 'right', msgText);
        }else{
            this.appendMessage(config['to_user_name'], config['to_user_img'], 'left', msgText);
            socket.emit('set_single_message_as_read', {'message_id': data['message_id']});
        }
    }
}


function increment_badge(chat_badge){
    const current_val = Number(chat_badge.text());
    chat_badge.html(`<strong>${current_val+1}</strong>`);
}


function reduce_badge(data, chat_badge){
    const current_val = Number(chat_badge.text());
    const to_reduce = Number(data['count']);
    const reduced = current_val - to_reduce;
    chat_badge.html(`<strong>${reduced > 0 ? reduced: 0}</strong>`);
}


function appendMessage(data, url_path){
    const url = `${url_path}/${data['user_pk']}`;
    const msg = `
			<a href="${url}" class="dropdown-item">
				<!-- Message Start -->
				<div class="media">
					<img src="${data['user_photo']}" alt="Аватар пользователя" class="img-size-50 mr-3 img-circle dropdown-chat-avatar">
					<div class="media-body">
						<h3 class="dropdown-item-title">
							${data['user_full_name']}
							<span class="float-right text-sm text-danger"><i class="fas fa-star"></i></span>
						</h3>
						<p class="text-sm">${data['text']}</p>
						<p class="text-sm text-muted"><i class="far fa-clock mr-1"></i> ${data['created_time']}</p>
					</div>
				</div>
				<!-- Message End -->
			</a>`;
    CHAT_DROPDOWN_MENU.prepend(msg);
}
