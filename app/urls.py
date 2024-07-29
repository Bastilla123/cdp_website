

from django.urls import path, re_path
from app import views
from customers.views import home

urlpatterns = [

    # The home page
    path('', home, name='home'),
    path('/', home, name='home'),

    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),

]
