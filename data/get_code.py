# -*- coding: utf-8 -*-
import requests


class GetCode:

    @staticmethod
    def get_code():
        cod = requests.get("http://192.168.22.162/vc")
        assert cod.status_code == 200, f"Ошибка получения кода, фактический статус получения кода ='{cod.status_code}'"
        return cod.json()["verify_code"]
