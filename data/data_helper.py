# -*- coding: utf-8 -*-
import random

from mimesis import Person, Finance, Address, Code, Text

name = Person("ru")
email = Person("en")
password = Person().password(8)
short_password = Person().password(6)
rep_password = Person().password(8)
company = Finance("ru")
device = ['Сигнал - Р', 'CИРИУС', 'КД', 'Протон', 'Ангара', 'Байкал', 'Сигнал - Л']
status = [1, 2, 3, 4, 5]
active = ['false', 'true']
adress = Address("ru")
numbers = Code()
text = Text("ru")

number = random.randint(1111111111111, 9999999999999)

ip = '192.168.22.103'

fiz_user = {
    "email": "user_bolid_10@localhost.ru",
    "password": "bolid_999999"
}

ur_user = {
    "email": "user_bolid_ur@localhost.ru",
    "password": "bolid_999999"
}

url = "http://127.0.0.1:8000"
host = "127.0.0.1:8000"

real_device = {
    "id_dev": "1",
    "name": company.company(),
    "status": random.choice(status),
    "address": adress.address(),
    "type_num": 1,
    "type_text": text.text(1),
    "is_active": random.choice(active)
}

random_device = {
    "id_dev": numbers.imei(),
    "name": company.company(),
    "status": random.choice(status),
    "address": adress.address(),
    "type_num": 1,
    "type_text": text.text(1),
    "is_active": random.choice(active)
}

data_vev = {
    "id_dev": "1",
    "name": "string",
    "status": 1,
    "address": "string",
    "type_num": 1,
    "is_active": "true"
}


class ExceptionError(Exception):
    pass
