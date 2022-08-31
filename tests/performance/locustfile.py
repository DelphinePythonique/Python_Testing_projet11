from locust import HttpUser, task, between

from tests.conftest import EMAIL_OK, CLUB_OK, COMPETITION_OK


class ServerPerfTest(HttpUser):
    wait_time = between(5, 15)

    @task(10)
    def index(self):
        self.client.get("/")

    @task
    def show_summary(self):
        self.client.post("/showSummary", {"email": EMAIL_OK})

    @task(8)
    def book(self):
        self.client.get("/book/competition test1/test1")

    @task(5)
    def purchase_place(self):
        self.client.post("/purchasePlaces", {"club": CLUB_OK, "competition": COMPETITION_OK, "places": 1})