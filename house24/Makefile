docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

db-migrate:
	docker-compose exec web python manage.py migrate

run_chat_app:
	python chat_app/server.py
