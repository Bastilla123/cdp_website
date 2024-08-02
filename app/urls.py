

from django.urls import path, re_path
from app import views
from customers.views import *
from .views import *

urlpatterns = [

    # The home page
    path('', home, name='home'),
    path('/', home, name='home'),
    path('log/', log_view, name='log_view'),

    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),

]
