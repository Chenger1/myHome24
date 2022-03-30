docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

db-migrate:
	docker-compose exec web python manage.py migrate

chat:
	cd chat_app && gunicorn -k geventwebsocket.gunicorn.workers.GeventWebSocketWorker -w 1 server:app -b 127.0.0.1:5000 --reload

chat-local:
	cd chat_app && python server.py
