import json
from random import randint
from locust import HttpLocust, TaskSet

home_url = "http://127.0.0.1:8000/api/v1/home/"
signup_url = "http://127.0.0.1:8000/api/v1/users/"
login_url = "http://127.0.0.1:8000/api/v1/login/"
flights_url = "http://127.0.0.1:8000/api/v1/flights/"
books_url = "http://127.0.0.1:8000/api/v1/books/"


def index(l):
    l.client.get(home_url)


def signup(l):
    username = ("allison{}{}".format(randint(1, 100), randint(0, 999)),)
    password = "Password{}{}?".format(randint(1, 100), randint(0, 999))
    email = "ifemi{0}{1}@gmail.com".format(randint(1, 100), randint(0, 999))

    l.client.post(
        signup_url,
        {
            "email": email,
            "first_name": "Alice",
            "last_name": "Otedom",
            "username": username,
            "password": password,
        },
    )


def login(l):
    l.client.post(login_url, {"username": "emmatope", "password": "Password92?"})


def flight(l):

    departure = ("2019-05-27 15:00:00+01",)
    arrival = ("2019-05-28 16:00:00+01",)
    fly_from = "Kano{}".format(randint(1, 1000))
    fly_to = "Abuja{}".format(randint(1, 1000))

    auth_response = l.client.post(
        login_url, {"username": "emmatope", "password": "Password92?"}
    )
    token = json.loads(auth_response.text)["token"]

    l.client.post(
        flights_url,
        {
            "departure": departure,
            "arrival": arrival,
            "fly_from": fly_from,
            "fly_to": fly_to,
            "capacity": 200,
        },
        headers={"Authorization": "JWT " + token},
    )


def book(l):
    flight_class = "FIRST"
    flight = gen_book_flight_id()

    auth_response = l.client.post(
        login_url, {"username": "emmatope", "password": "Password92?"}
    )
    token = json.loads(auth_response.text)["token"]
    l.client.post(
        books_url,
        {"flight_class": flight_class, "flight": 66},
        headers={"Authorization": "JWT " + token},
    )


class UserBehavior(TaskSet):
    tasks = {index: 1, login: 2, flight: 3, book: 4}

    def on_start(self):
        signup(self)

    def on_stop(self):
        index(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
