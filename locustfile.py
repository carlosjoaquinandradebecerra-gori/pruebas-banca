# locustfile.py
from locust import HttpUser, task, between

class BankUser(HttpUser):
    wait_time = between(1,3)

    def on_start(self):
        self.client.get("/parabank/index.htm")

    @task(3)
    def view_home(self):
        self.client.get("/parabank/index.htm", name="Home")

    @task(1)
    def transfer(self):
        self.client.post("/parabank/transfer.htm", {
            "amount": "1",
            "fromAccountId": "12345",
            "toAccountId": "67890"
        }, name="Transfer")
