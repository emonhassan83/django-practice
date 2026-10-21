from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    return render(request, "home.html")

def no_permission(request):
    return render(request, "no-permission.html")

def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect("sign-in")

    if request.user.is_superuser or request.user.groups.filter(name="Admin").exists():
        return redirect("admin-dashboard")
    elif request.user.groups.filter(name="Manager").exists():
        return redirect("manager_dashboard")
    else:
        return redirect("user_dashboard")
