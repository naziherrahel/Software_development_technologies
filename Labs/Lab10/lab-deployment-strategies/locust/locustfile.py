from locust import HttpUser, between, task


class DeploymentUser(HttpUser):
    wait_time = between(0.5, 2.0)

    @task
    def open_home_page(self):
        self.client.get("/", name="GET /")
