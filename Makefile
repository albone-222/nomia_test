DC = docker compose
APP_DB_FILE = app_db.yaml
APP_FILE = app.yaml

.PHONY: app-no-db
app-no-db:
	${DC} -f ${APP_FILE} up -d

.PHONY: drop-app-no-db
drop-app-no-db:
	${DC} -f ${APP_FILE} down	

.PHONY: app
app:
	${DC} -f ${APP_DB_FILE} up -d

.PHONY: drop-app
drop-app:
	${DC} -f ${APP_DB_FILE} down	