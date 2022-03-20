import time
import json
import random
from locust import HttpUser, task, between


class WebsiteUser(HttpUser):

    #wait_time = between(1, 2)

    @task(1)
    def get_cars(self):
        self.client.get("/cars")

    @task(1)
    def get_car_by_id(self):
        cars = self.client.get("/cars").json()
        req="/cars/"+cars[random.randint(1,len(cars)-1)]["_id"]
        #req="/cars/"+self.client.get("/cars").json()[0]["_id"]
        self.client.get(req)

    @task(1)
    def post_cars(self):
        self.client.post("/cars", json={
                "model": "POST test",
                "color": "test color",
                "horsepower": "100",
                "weight": "3.0",
                "1/4 mile time": "18.08",
                "cylinders": "8",
                "transmission": "Manual",
                "gears": "3"
            })

    @task(1)
    def put_cars(self):
        #cars = self.client.get("/cars").json()
        #req="/cars/"+cars[random.randint(1,len(cars)-1)]["_id"]
        req="/cars/"+self.client.get("/cars").json()[-1]["_id"]

        self.client.put(req, json={
                "model": "PUT test",
                "color": "test color",
                "horsepower": "100",
                "weight": "3.0",
                "1/4 mile time": "18.08",
                "cylinders": "8",
                "transmission": "Manual",
                "gears": "3"
            })

    @task(1)
    def delete_car(self):
        cars = self.client.get("/cars").json()
        #req="/cars/"+self.client.get("/cars").json()[-1]["_id"]
        req="/cars/"+cars[random.randint(1,len(cars)-1)]["_id"]

        self.client.delete(req)
