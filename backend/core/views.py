from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from django.db.models import Q, Prefetch
from .utils import *


class NewOrderCreateView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        queryset = Cell.objects.filter(free_place=1.0).prefetch_related('orders')
        if not queryset:
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
    queryset = User.objects.filter(telegram_id__isnull=False).only('telegram_id', 'phone', )
    serializer_class = TBUserSerializer


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