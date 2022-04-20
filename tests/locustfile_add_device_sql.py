# -*- coding: utf-8 -*-
from locust import HttpUser, task

from data.data_helper import *


class AdddeviceSql(HttpUser):
    def on_start(self):
        self.client.get("/login")

    @task
    def add_device(self):
        response1 = self.client.post(f"{url}/auth/jwt/create/", fiz_user)
        token = response1.json()['access']
        _headers = {"Authorization": "JWT " + token}
        _random_device = {
            "id_dev": numbers.imei(),
            "name": company.company(),
            "status": random.choice(status),
            "address": adress.address(),
            "type_num": 1,
            "type_text": text.text(1),
            "is_active": random.choice(active)
        }
        with self.client.post(f"{url}/devices/", headers=_headers, data=_random_device,
                              catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Ошибка! Запрос на добавление устройства  /devices/ не возможен! Тело ответа:'{response.text}' \n Код:'{response.status_code}'")
                raise ExceptionError("Сценарий провален! Не выполнен запрос на добавление устройства")
