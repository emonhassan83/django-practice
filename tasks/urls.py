from django.urls import path
from tasks.views import manager_dashboard, user_dashboard, home, task_form

urlpatterns = [
    path("", home, name="home"),
    path("manager-dashboard/", manager_dashboard, name="manager_dashboard"),
    path(
        "manager-dashboard/<str:status>/",
        manager_dashboard,
        name="manager_dashboard_by_status",
    ),
    path("user-dashboard/", user_dashboard, name="user_dashboard"),
    path("task-form/", task_form, name="task_form"),
]
