DJANGO_SETTINGS_MODULE=project.settings
DOCKER_COMPOSE_DEV=conf/docker-compose_dev.yml
CELERY_SERVICES=-A project
CELERY_PID_FILE=/tmp/celery.pid
CELERY_LOG_FILE=/tmp/broker.log

.PHONY: init
init: export_settings
	@echo "Initiliazing application's data and state"
	@make update-db
	@make start-services
	@make load-fixtures
	@echo "\nAddress: http://localhost:8000/admin"
	@echo "Credentials:\n  - user: admin\n  - pass: 123"

.PHONY: update-db
update-db:
	./manage.py makemigrations
	./manage.py migrate

.PHONY: export_settings
export_settings:
	export DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE)

# Remove migrations que não foram adicionados.
.PHONY: del-dev-migrations
del-dev-migrations:
	git status --porcelain | grep "^?? "  | sed -e 's/^[?]* //' | \egrep "\migrations/00*"  | xargs -n1 rm -f

.PHONY: down
down: del-dev-migrations
	rm -f db.sqlite3


.PHONY: save-fixtures
save-fixtures:
	./manage.py dumpdata notification.namespace > apps/notification/fixtures/000_namespace.json
	./manage.py dumpdata notification.group > apps/notification/fixtures/001_group.json
	./manage.py dumpdata notification.subscriber > apps/notification/fixtures/002_subscriber.json
	./manage.py dumpdata notification.device > apps/notification/fixtures/003_device.json
	./manage.py dumpdata notification.notification > apps/notification/fixtures/004_notification.json


# Adiciona fixtures
.PHONY: load-fixtures
load-fixtures:
	./manage.py loaddata 000_admin
	./manage.py loaddata 000_namespace
	./manage.py loaddata 001_group
	./manage.py loaddata 002_subscriber
	./manage.py loaddata 003_device
	./manage.py loaddata 004_notification


.PHONY: broker_create
broker_create: broker_kill
	celery -E $(CELERY_SERVICES) worker -B -l INFO --scheduler django -s /tmp/beat-scheduler --logfile="$(CELERY_LOG_FILE)" --pidfile="$(CELERY_PID_FILE)" --detach;


.PHONY: broker_kill
broker_kill:
	ps x --no-header -o pid,cmd | awk '!/awk/&&/celery/{print $$1}' | xargs -r kill
	rm -f $(CELERY_PID_FILE)


.PHONY: broker_restart
broker_restart:
	@make broker_kill
	@make broker_create


.PHONY: broker_debug
broker_debug: broker_kill
	celery -E $(CELERY_SERVICES) worker -B -l INFO --scheduler django -s /tmp/beat-scheduler --logfile="$(CELERY_LOG_FILE)" --pidfile="$(CELERY_PID_FILE)";


.PHONY: broker_logs
broker_logs:
	touch $(CELERY_LOG_FILE)
	tail -f  $(CELERY_LOG_FILE)


.PHONY: start-services
start-services: broker_create
	docker-compose -f $(DOCKER_COMPOSE_DEV) up -d --remove-orphans;

.PHONY: stop-services
stop-services:
	docker-compose -f $(DOCKER_COMPOSE_DEV) stop;

.PHONY: destroy-services
destroy-services: broker_kill
	docker-compose -f $(DOCKER_COMPOSE_DEV) down;

.PHONY: logs
logs:
	docker-compose -f $(DOCKER_COMPOSE_DEV) logs -f

.PHONY: services
services:
	docker-compose -f $(DOCKER_COMPOSE_DEV) ps