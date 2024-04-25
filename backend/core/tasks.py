from backend.celery import app
from django.db.models import Avg, Sum, Count

from .models import *
from .service import *


@app.task
def order_deadline():
    orders = Order.objects.filter(expiration_date=deadline_date())
    for order in orders:
        if order.user.telegram_id:
            deadline_message(order_id=order.pk, telegram_id=order.user.telegram_id)
    return None


@app.task
def employee_rating():
    employers = Employee.objects.all()
    for employee in employers:
        sum = 0
        comments = Comment.objects.filter(employee=employee.pk)
        for comment in comments:
            sum += comment.rating
        employee.rating = sum/len(comments)

        employee.save()
