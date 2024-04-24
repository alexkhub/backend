from backend.celery import app
from .models import *
from .service import *


@app.task
def order_deadline():
    orders = Order.objects.filter(expiration_date=deadline_date())
    for order in orders:
        if order.user.telegram_id:
            deadline_message(order_id=order.pk, telegram_id=order.user.telegram_id)
    return None

