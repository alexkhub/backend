from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField('username', queryset=User.objects.all())

    class Meta:

        model = Order
        fields = '__all__'

    def create(self, validated_data):

        validated_data['user'] = self.context['request'].user
        size = validated_data['order_size']

        order = Order.objects.create(**validated_data)
        if size == 'маленький заказ':
            cell = Cell.objects.filter(free_place__gte=0.5).first()
        elif size == 'большой заказ':
            cell = Cell.objects.filter(free_place=1).first()

        if cell:
            cell.orders.add(order)
            cell.save()
            if cell.free_place < 0:
                return serializers.ValidationError('ячейка заполнена')
        else:
            return serializers.ValidationError('ячейки заполнены')
        return order


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'


class TBUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id', 'phone',)


class TBOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password',  'repeat_password', 'first_name', 'last_name', 'email', 'phone', 'telegram_id')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password, repeat_password = attrs.get('password', None), attrs.pop('repeat_password', None)

        if password is None or repeat_password is None:
            raise serializers.ValidationError("Вы забыли заполнить пароль")
        if password != repeat_password:
            raise serializers.ValidationError("Пароль не совпадает")

        return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ('date',)

    def create(self, validated_data):

        return Comment.objects.create( **validated_data)

class TBGETIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'telegram_id')


class StatisticEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model  = Employee
        fields = ('user', 'rating')