from django.urls import path
from users.views import sign_up, sign_in, sign_out, activate_user, admin_dashboard, assign_role, create_group

urlpatterns = [
    path("sign-up", sign_up, name='sign-up'),
    path("sign-in", sign_in, name='sign-in'),
    path("sign-out", sign_out, name='sign-out'),
    path("activate/<int:user_id>/<str:token>/", activate_user),
    path("admin-dashboard", admin_dashboard, name='admin-dashboard'),
    path("assign-role/<int:user_id>/", assign_role, name='assign-role'),
    path("create-group", create_group, name='create-group'),
]
