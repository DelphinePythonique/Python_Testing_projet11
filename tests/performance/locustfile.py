from locust import HttpUser, task, User, between


class ServerPerfTest(HttpUser):
    wait_time = between(5, 15)

    @task
    def index(self):
        self.client.get('/')
