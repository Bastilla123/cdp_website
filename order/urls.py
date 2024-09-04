from django.urls import path
from .views import *

app_name = 'order'

urlpatterns = [
    path('order/', order_line.as_view(), name = 'order'),

    path('execute_order/', execute_order, name = 'execute_order'),
    path('summary/', summary, name = 'summary'),
]


