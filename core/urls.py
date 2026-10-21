from django.urls import path
from core.views import home, no_permission, dashboard_redirect

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/", dashboard_redirect, name="dashboard"),
    path("no-permission/", no_permission, name="no-permission"),
]

