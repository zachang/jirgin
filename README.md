
# Jirgin

[![Build Status](https://travis-ci.org/zachang/jirgin.svg?branch=develop)](https://travis-ci.org/zachang/jirgin)
[![Coverage Status](https://coveralls.io/repos/github/zachang/jirgin/badge.svg?branch=develop)](https://coveralls.io/github/zachang/jirgin?branch=develop)

Jirgin is a flight booking API that enables users register, log in, upload profile image, receive email reminder, receive email reservation confirmation and check status of their flight.

## Project Setup

- Clone the repo.
- Change into the directory $ cd /bookings
- Create a .env file in your root directory as described in .env.sample file.
- Have at least Python 3.6.x installed.
- Create a virtual environment using `python -m venv venv-name-you-like` command.
- Activate virtual environment using `source venv-name-given/bin/activate`
- Run `make pip-install` to install dependencies.
- Run `make pre-commit` to activate the pre-commit hook for code formatting before commits are applied

## Migarations

- First setup database connections.
- Run `make migrate`.
- For new model changes run `make migrations` before `make migrate`.

## Running App

- Run `make runserver`

## Running Tests

- Run `make test

## Technologies Used

- [Django](https://www.djangoproject.com/) - Python web framework used
- [Django rest framework](https://www.django-rest-framework.org/) - Used for rapidly building RESTful APIs based on Django models.
- [Postgres](https://www.postgresql.org/) - Object-relational database used
- [Cloudinary](https://cloudinary.com/) - Cloud platform used for file management like images, videos etc.

## How To Contribute
- Fork this repository to your GitHub account
- lone the forked repository
- Create your feature branch
- Commit your changes
- Push to the remote branch
- Open a Pull Request

## Author
- Dawuda Ebenezer Zachang