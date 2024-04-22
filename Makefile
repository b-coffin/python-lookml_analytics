include .env

# gcloudの認証ファイル取得
get-gcloud-auth-json:
	gcloud auth application-default login --disable-quota-project

# Docker

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down --rmi all --volumes

docker-exec-db:
	docker compose exec db bash

# DB

login-db:
	docker compose exec db mysql -u root -h localhost -P 3306 -D $(MYSQL_DATABASE) -p$(MYSQL_ROOT_PASSWORD)

login-psgl:
	docker compose exec postgres psql -U $(POSTGRES_USER) -h localhost -d $(POSTGRES_DB)

# APP

main:
	@docker compose exec app python main.py
