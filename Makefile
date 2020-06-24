DJANGO_SETTINGS_MODULE=project.settings

.PHONY: init
init: export_settings
	@echo "Initiliazing application's data and state"
	./manage.py makemigrations notification
	./manage.py migrate
	./manage.py loaddata 000_admin
	@echo "\nAddress: http://localhost:8000/admin"
	@echo "Credentials:\n  - user: admin\n  - pass: 123"

.PHONY: export_settings
export_settings:
	export DJANGO_SETTINGS_MODULE=$(DJANGO_SETTINGS_MODULE)

.PHONY: down
down:
	rm -f db.sqlite3
