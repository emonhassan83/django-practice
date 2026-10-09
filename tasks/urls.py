from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, home

urlpatterns = [
    path("", home, name="home"),
    path("manager-dashboard/", manager_dashboard, name="manager_dashboard"),
    path("user-dashboard/", user_dashboard, name="user_dashboard"),
]