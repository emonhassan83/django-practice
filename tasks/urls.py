from django.urls import path, include
from tasks.views import (
    manager_dashboard,
    user_dashboard,
    task_form,
    update_task,
    delete_task,
)

urlpatterns = [
    path("manager-dashboard/", manager_dashboard, name="manager_dashboard"),
    path(
        "manager-dashboard/<str:status>/",
        manager_dashboard,
        name="manager_dashboard_by_status",
    ),
    path("user-dashboard/", user_dashboard, name="user_dashboard"),
    path("task-form/", task_form, name="task_form"),
    path("update-task/<int:id>/", update_task, name="update_task"),
    path("delete-task/<int:id>/", delete_task, name="delete_task")
]
