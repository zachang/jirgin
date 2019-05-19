PYTHON_MANAGE := python manage.py 

black:
	black ../bookings/

locust:
	locust --host=http://127.0.0.1:8000/

migrations:
	$(PYTHON_MANAGE) makemigrations

migrate:
	$(PYTHON_MANAGE) migrate

pip-install:
	pip install -r requirements.txt

pre-commit:
	pre-commit install

runserver:
	$(PYTHON_MANAGE) runserver

test:
	coverage run --source='.' manage.py test
	coverage report
	coverage html