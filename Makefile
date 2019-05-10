PYTHON_MANAGE := python manage.py 

black:
	black ../bookings/

pre-commit:
	pre-commit install

migrations:
	$(PYTHON_MANAGE) makemigrations

migrate:
	$(PYTHON_MANAGE) migrate

pip-install:
	pip install -r requirements.txt