from django.db import models

from django.contrib.auth.models import AbstractUser
from sortedm2m.fields import SortedManyToManyField
from autoslug import AutoSlugField
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
ORDER_STATUS = (
    ('выдан', 'выдан'),
    ('не выдан', 'не выдан')
)

ORDER_SIZE = (
    ('большой заказ', 'большой заказ'),
    ('маленький заказ', 'маленький заказ')
)


class User(AbstractUser):
    phone = models.CharField(max_length=15, verbose_name='Номер телефона')
    address = models.CharField(max_length=75, verbose_name='Адрес', blank=True)
    slug = AutoSlugField(populate_from='username', unique=True, db_index=True, verbose_name='URL', )
    telegram_id = models.CharField(max_length=200, verbose_name='telegram_id', blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    delivery_date = models.DateField(verbose_name='Дата доставки', auto_now_add=True)
    status = models.CharField(max_length=30, verbose_name='Статус', choices=ORDER_STATUS, default='не выдан')
    expiration_date = models.DateField(verbose_name='Дата истечения', blank=True, null=True)
    order_size = models.CharField(max_length=30, verbose_name='Размер заказа', choices=ORDER_SIZE,
                                  default='большой заказ')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.pk}"


class Employee(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.DecimalField(verbose_name='Рейтинг', max_digits=5, decimal_places=2, default=5)

    class Meta:
        verbose_name = 'Сотрудники'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return str(self.user)


class Cell(models.Model):
    orders = SortedManyToManyField('Order', verbose_name='Заказы', blank=True, null=True)
    free_place = models.FloatField(verbose_name='Свободное место', default=1, )

    class Meta:
        verbose_name = 'Ячейка'
        verbose_name_plural = 'Ячейки'

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):

        self.free_place = 1
        try:
            for order in self.orders.all():
                if self.free_place < 0:
                    return ValidationError("Заполнена")

                if order.order_size == 'маленький заказ':
                    self.free_place = self.free_place - 0.5
                elif order.order_size == 'большой заказ':
                    self.free_place = self.free_place - 1


        except:
            pass

        super(Cell, self).save(*args, **kwargs)



class Rack(models.Model):
    cells = SortedManyToManyField('Cell', verbose_name='Ячейки')
    employee = models.ForeignKey('Employee', verbose_name='Сотрудник', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Стеллаж'
        verbose_name_plural = 'Стеллажи'

    def __str__(self):
        return str(self.pk)


class Stock(models.Model):
    area = models.PositiveIntegerField(verbose_name='Площадь', default=0)
    address = models.CharField(max_length=75, verbose_name='Адрес', blank=True)
    racks = SortedManyToManyField('Rack', verbose_name='Стеллажи')
    employers = SortedManyToManyField('Employee', verbose_name='Сотрудники')
    slug = AutoSlugField(populate_from='address', unique=True, db_index=True, verbose_name='URL', )

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склад'

    def __str__(self):
        return self.address


class Comment(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="Пользователь")
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    rating = models.PositiveIntegerField(verbose_name='Оценка', default=5)
    date = models.DateField(verbose_name='Время', auto_now_add=True, blank=True)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return f'{self.user} - {self.date}'
