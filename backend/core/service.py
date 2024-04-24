from datetime import datetime, date, timedelta

import requests
from django.core.mail import send_mail
from .models import *

def deadline_date():
    return date.today() + timedelta(days=1)


def deadline_message(telegram_id, order_id ) :

    url = 'http://192.168.77.83:8000/api-tg/productDeadline/'
    requests.post(url=url, json= {
        "telegram_id": telegram_id,
        "order_id": order_id,
        "address": "Где-то там"
}, headers={'Content-Type': "application/json"})