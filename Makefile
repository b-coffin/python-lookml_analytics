# Docker

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down --rmi all --volumes

# ファイル実行

getfields:
	@docker compose exec app python getfields.py

comparefields:
	@docker compose exec app python comparefields.py
