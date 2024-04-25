from django.urls import path

from .views import *

urlpatterns = [
    path('new_order/', NewOrderCreateView.as_view(), name = 'new_order'),
    path('free_cell/', FreeCellListView.as_view() , name='free_cell'),
    path('tb_users/', TBUserListView.as_view(), name='tb_users'),
    path('tb_orders/<slug:telegram_id>/', TBMyOrdersListView.as_view(), name='tb_orders'),
    path('create_user/', UserRegistrationCreateView.as_view(), name='create_user'),
    path('create_comment/', CommentCreateView.as_view(), name='create_comment' ),
    path('tb_check_id/<slug:telegram_id>/', TBGETIDRetrieveView.as_view(), name='tb_check_id'),
    path('igor_orders/<slug:phone>/', IgorCheckListView.as_view(), name='igor_orders'),
    path('igor_order_detail/<int:id>/', IgorOrderRetrieveView.as_view(), name='igor_order_detail'),
    path('statistics/', StatisticsListView.as_view(), name='statistics/'),
    path('statistic_employee/', StatisticEmployeeListView.as_view() , name='statistic_employee'),
    path('a/', OrderStatisticListView.as_view(), name='order_statistic')

]