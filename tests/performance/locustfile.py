from locust import HttpUser, task, between

from tests.conftest import EMAIL_OK


class ServerPerfTest(HttpUser):
    wait_time = between(5, 15)

    @task(10)
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        self.client.post("/showSummary", {"email": EMAIL_OK})
