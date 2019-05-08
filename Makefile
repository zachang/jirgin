black:
	black ../bookings/

pre-commit:
	pre-commit install

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate