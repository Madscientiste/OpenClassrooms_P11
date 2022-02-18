from locust import HttpUser, task, between
import random

from app.data import clubs, competitions


class User(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def view_clubs(self):
        self.client.get("/clubs")

    @task(1)
    def view_index(self):
        self.client.get("/")

    @task(2)
    def login(self):
        club_email = clubs.get_random("email")
        self.client.post("/summary", {"email": club_email})

    @task(2)
    def booking_page(self):
        competition = competitions.get_random("name")
        club = clubs.get_random("name")
        self.client.get(f"/book/{competition}/{club}")

    @task(3)
    def confirm_booking(self):
        req_seats = random.randint(1, 12)
        competition = competitions.get_random("name")
        club = clubs.get_random("name")

        self.client.post("/confirm_booking", {"competition": competition, "club": club, "seats": req_seats})
