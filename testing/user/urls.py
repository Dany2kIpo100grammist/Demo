from django.contrib import admin
from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path('login/', views.login_view, name="login"),
    path('register/', views.register_view, name="register"),
    path('requests/', views.requests_view, name="requests"),
    path('requests/history/', views.requests_history_view, name="requests_history")
]