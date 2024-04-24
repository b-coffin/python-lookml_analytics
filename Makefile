# Docker

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down --rmi all --volumes

docker-exec-db:
	docker compose exec db bash

# APP

main:
	@docker compose exec app python main.py
