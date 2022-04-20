# -*- coding: utf-8 -*-
import asyncio
import json

import websockets
from locust import HttpUser, task

from data.data_helper import *
from data.get_code import GetCode


class Adddevice(HttpUser, GetCode):
    def on_start(self):
        self.client.get("/login")

    @task
    def add_device_ws(self):
        async def listen():
            websocket_resource_url = f"ws://{ip}/ws/routing/1-{number}/"
            async with websockets.connect(websocket_resource_url) as ws:
                await ws.send('{"method":"device_status","params":{}}')
                # WS №1
                msg = await ws.recv()
                ws_res_1 = json.loads(msg)
                if ws_res_1['params'] == {'status': 2}:
                    # WS №2
                    await ws.send('{' + f'"method":"verify_code","params":"{self.get_code()}"' + '}')
                    msg2 = await ws.recv()
                    ws_res_22 = json.loads(msg2)
                    if ws_res_22['params'] == {'status': 2}:
                        await ws.send('{' + f'"method":"verify_code","params":"{self.get_code()}"' + '}')
                        msg2 = await ws.recv()
                        ws_res_222 = json.loads(msg2)
                        assert ws_res_222['params'] == {
                            'status': 1}, f"Ошибка ответа при отправке WS №2, тело ответа:'{ws_res_222}'"
                else:
                    websocket_resource_url = f"ws://{ip}/ws/routing/1-{number}/"
                    async with websockets.connect(websocket_resource_url) as ws:
                        await ws.send('{"method":"device_status","params":{}}')
                        # WS №1
                        msg = await ws.recv()
                        ws_res_1 = json.loads(msg)
                        assert ws_res_1['params'] == {
                            'status': 2}, f"Ошибка ответа при отправке WS №1, тело ответа:'{ws_res_1}'"
                        # WS №2
                        await ws.send('{' + f'"method":"verify_code","params":"{self.get_code()}"' + '}')
                        msg2 = await ws.recv()
                        ws_res_2 = json.loads(msg2)
                        assert ws_res_2['params'] == {
                            'status': 1}, f"Ошибка ответа при отправке WS №2, тело ответа:'{ws_res_2}'"

        asyncio.run(listen())

    @task
    def add_device_client(self):
        response1 = self.client.post(f"{url}/auth/jwt/create/", fiz_user)
        token = response1.json()['access']
        _headers = {"Authorization": "JWT " + token}
        with self.client.post(f"{url}/devices/", data=data_vev, headers=_headers, catch_response=True) as response:
            if response.status_code == 200 or response.status_code == 201:
                response.success()
            else:
                response.failure(
                    f"Ошибка! Запрос на добавление устройства  /devices/ не возможен! Тело ответа:'{response.text}'"
                    f" \n Код:'{response.status_code}'")
                raise ExceptionError("Сценарий провален! Не выполнен запрос на добавление устройства")
        with self.client.get(f"{url}/devices/1/search/", headers=_headers, catch_response=True) as response1:
            if response1.status_code == 200 or response1.status_code == 201:
                response1.success()
            else:
                response1.failure(
                    f"Ошибка! Запрос на поиск устройства  /devices/1/search/ не возможен! Тело ответа:'{response1.text}'"
                    f" \n Код:'{response1.status_code}'")
                raise ExceptionError("Сценарий провален! Не выполнен запрос на поиск устройства")
