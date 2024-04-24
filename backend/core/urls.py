from django.urls import path

from .views import *

urlpatterns = [
    path('new_order/', NewOrderCreateView.as_view(), name = 'new_order'),
    path('free_cell/', FreeCellListView.as_view() , name='free_cell'),
    path('tb_users/', TBUserListView.as_view(), name='tb_users'),
    path('tb_orders/<slug:telegram_id>/', TBMyOrdersListView.as_view(), name='tb_orders'),
    path('create_user/', UserRegistrationCreateView.as_view(), name='create_user'),
    path('create_comment/', CommentCreateView.as_view(), name='create_comment' )


]