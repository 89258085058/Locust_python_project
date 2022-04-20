# -*- coding: utf-8 -*-
import string

from locust import HttpUser, task

from data.data_helper import *


class UserData(HttpUser):
    def on_start(self):
        self.client.get("/login")

    @task
    def change_user_fiz_data(self):
        response1 = self.client.post(f"{url}/auth/jwt/create/", fiz_user, catch_response=True)
        token = response1.json()['access']
        _headers = {"Authorization": "JWT " + token}
        data_user = {
            "first_name": str(random.choice(string.ascii_letters) * random.randint(10, 20)),
            "last_name": str(random.choice(string.ascii_letters) * random.randint(5, 15)),
            "second_name": str(random.choice(string.ascii_letters) * random.randint(5, 15)),
            "type_user": "legal"
        }
        with self.client.patch(f"{url}/auth/users/me/", headers=_headers, data=data_user,
                               catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Ошибка! Запрос на изменение личных данных /auth/users/me/ не возможен! Тело ответа:'{response.text}' \n Код:'{response.status_code}'")
                raise ExceptionError("Сценарий провален! Не выполнен запрос на на изменение личных данных")

    @task
    def change_user_ur_data(self):
        response1 = self.client.post(f"{url}/auth/jwt/create/", ur_user, catch_response=True)
        token = response1.json()['access']
        _headers = {"Authorization": "JWT " + token}
        data = {
            "first_name": str(random.choice(string.ascii_letters) * random.randint(10, 20)),
            "last_name": str(random.choice(string.ascii_letters) * random.randint(5, 15)),
            "second_name": str(random.choice(string.ascii_letters) * random.randint(5, 15)),
            "type_user": "legal",
            "profile": {
                "organization_name": company.company(),
                "boss_post": name.academic_degree(),
                "legal_full_address": adress.address(),
                "legal_postal_code": random.randint(1111111, 9999999),
                "legal_region": adress.region(),
                "legal_city": adress.city(),
                "legal_street": adress.street_name(),
                "postal_full_address": adress.address(),
                "postal_postal_code": random.randint(1111111, 9999999),
                "postal_region": adress.region(),
                "postal_city": adress.city(),
                "inn": random.randint(11111111111, 99999999999),
                "kpp": random.randint(111111111, 999999999)
            }
        }
        with self.client.patch(f"{url}/auth/users/me/", headers=_headers, data=data, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Ошибка! Запрос на изменение личных данных /auth/users/me/ не возможен! Тело ответа:'{response.text}' \n Код:'{response.status_code}'")
                raise ExceptionError("Сценарий провален! Не выполнен запрос на на изменение личных данных")
