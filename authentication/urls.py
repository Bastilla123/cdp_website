# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("contact/", contact, name="contact"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard", dashboard, name="dashboard"),
    path("cost", cost, name="cost"),
    path("emissions", emissions, name="emissions"),
    path("documents", documents, name="documents")

]
