DJANGO_SETTINGS_MODULE=project.settings

.PHONY: init
init: export_settings
	@echo "Initiliazing application's data and state"
	./manage.py makemigrations
	./manage.py migrate
	@make load-fixtures
	@echo "\nAddress: http://localhost:8000/admin"
	@echo "Credentials:\n  - user: admin\n  - pass: 123"

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
	./manage.py dumpdata notification.transmission > apps/notification/fixtures/005_transmission.json


# Adiciona fixtures
.PHONY: load-fixtures
load-fixtures:
	./manage.py loaddata 000_admin
	./manage.py loaddata 000_namespace
	./manage.py loaddata 001_group
	./manage.py loaddata 002_subscriber
	./manage.py loaddata 003_device
	./manage.py loaddata 004_notification
	./manage.py loaddata 005_transmission
