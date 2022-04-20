# -*- coding: utf-8 -*-
from locust import HttpUser, task

from data.data_helper import *


class FizUser(HttpUser):
    def on_start(self):
        self.client.get("/login")

    @task(1)
    def auth(self):
        with self.client.post("/auth/jwt/create/", fiz_user, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Ошибка! Запрос на авторизацию /auth/jwt/create/ не возможен! Тело ответа:'{response.text}'")
                raise ExceptionError("Сценарий провален!")

    @task(10)
    def go_to_object_page(self):
        self.client.get("/facilities")

    @task(5)
    def go_to_divice_page(self):
        self.client.get("/devices")

    @task(1)
    def go_to_data_user_page(self):
        self.client.get("/user_settings")
