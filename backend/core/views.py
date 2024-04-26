from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.db.models import Q, Prefetch
from .utils import *
from .service import *


class NewOrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        queryset1 = Cell.objects.filter(free_place=1.0).prefetch_related('orders')
        if not queryset1:
            return Response({'message': 'Нет свободного места'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FreeCellListView(ListAPIView):
    queryset = Cell.objects.filter(free_place__gt=0).prefetch_related('orders')
    serializer_class = CellSerializer


class TBUserListView(ListAPIView):
    queryset = User.objects.filter(telegram_id__isnull=False).only('telegram_id', 'phone', 'id')
    serializer_class = TBUserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TBMyOrdersListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = TBOrderSerializer

    def get_queryset(self):
        self.queryset = self.queryset.filter(user__telegram_id=self.request.resolver_match.kwargs['telegram_id'])
        return self.queryset


class UserRegistrationCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        print(request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TBGETIDRetrieveView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = TBGETIDSerializer

    lookup_field = 'telegram_id'


class IgorCheckListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        self.queryset = self.queryset.filter(user__phone=self.request.resolver_match.kwargs['phone'])
        return self.queryset


class StatisticsListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        new_order = len(self.get_queryset().filter(delivery_date=get_date()))
        completed_orders = len(self.get_queryset().filter(status='выдан'))
        free_cell = len(Cell.objects.filter(free_place=1.0).prefetch_related('orders'))
        cell = len(Cell.objects.all().prefetch_related('orders'))
        expiration_orders = len(self.get_queryset().filter(expiration_date=get_date()))
        return Response({'new_order': new_order,
                         'completed_orders': completed_orders,
                         'cell': cell,
                         'free_cell': free_cell,
                         'expiration_orders' : expiration_orders
                         }
                        )


class IgorOrderRetrieveView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    lookup_field = 'id'


class StatisticEmployeeListView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = StatisticEmployeeSerializer


class OrderStatisticListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        order_count = len(self.get_queryset())
        completed_orders = len(self.get_queryset().filter(status='выдан'))
        return Response({'order_count': order_count,
                         'completed_orders': completed_orders, })
