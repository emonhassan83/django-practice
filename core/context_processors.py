def role_context(request):
    user = request.user
    if not user.is_authenticated:
        return {
            "is_admin": False,
            "is_manager": False,
            "is_employee": False,
            "dashboard_url": "sign-in",
            "dashboard_name": "Sign In",
        }

    is_admin = user.is_superuser or user.groups.filter(name="Admin").exists()
    is_manager = is_admin or user.groups.filter(name="Manager").exists()
    is_employee = (
        user.groups.filter(name__in=["Employee", "User"]).exists()
        or not (is_admin or is_manager)
    )

    if is_admin:
        dashboard_url = "admin-dashboard"
        dashboard_name = "Admin Dashboard"
    elif is_manager:
        dashboard_url = "manager_dashboard"
        dashboard_name = "Manager Dashboard"
    else:
        dashboard_url = "user_dashboard"
        dashboard_name = "User Dashboard"

    return {
        "is_admin": is_admin,
        "is_manager": is_manager,
        "is_employee": is_employee,
        "dashboard_url": dashboard_url,
        "dashboard_name": dashboard_name,
    }
