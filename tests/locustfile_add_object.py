# -*- coding: utf-8 -*-
import json

import requests
from locust import HttpUser, task

from data.data_helper import *


class AddObject(HttpUser):
    def on_start(self):
        self.client.get("/login")

    @task
    def add_object(self):
        response1 = requests.post(f"{url}/auth/jwt/create/", fiz_user)
        token = response1.json()['access']
        _headers = {"Authorization": "JWT " + token, 'Content-type': 'application/json'}
        _headers1 = {"Authorization": "JWT " + token}
        _random_device = {
            "id_dev": numbers.imei(),
            "name": company.company(),
            "status": random.choice(status),
            "address": adress.address(),
            "type_num": 1,
            "type_text": text.text(1),
            "is_active": random.choice(active)
        }
        response2 = requests.post(f"{url}/devices/", headers=_headers1, data=_random_device)
        id = response2.json()["id_dev"]
        data = {
            "name": company.company(),
            "address": adress.address(),
            "devices": [{
                "id_dev": id,
                "name": company.company(),
                "status": '1',
                "address": adress.address(),
                "type_num": '1',
                "is_active": '1'}]
        }
        data_json = json.dumps(data)
        with self.client.post("/facilities/", headers=_headers, data=data_json, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Ошибка! Запрос на добавление объекта  /devices/ не возможен! Тело ответа:'{response.text}' \n Код:'{response.status_code}'")
                raise ExceptionError("Сценарий провален! Не выполнен запрос на добавление объекта")
