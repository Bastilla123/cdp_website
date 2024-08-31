from django.urls import path
from customers import views
from .views import *

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('api/profile/', APIProfileView.as_view()),
    path('api/profile', APIProfileView.as_view()),
    path("contactus", contactus, name="contactus")

]
