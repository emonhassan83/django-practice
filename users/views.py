from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User, Group
from django.contrib import messages
from users.form import CustomSignUpForm, SignInForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test

# Test User
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())

def sign_up(request):
    if request.method == "POST":
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(
                request,
                f"We have sent an activation email to {user.email}. Click the link to activate your account.",
            )
            return redirect("sign-in")
    else:
        form = CustomSignUpForm()

    return render(request, "signup/signup.html", {"form": form})


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get("next") or request.POST.get("next")
            if next_url:
                return redirect(next_url)

            if user.is_superuser or user.groups.filter(name="Admin").exists():
                return redirect("admin-dashboard")
            elif user.groups.filter(name="Manager").exists():
                return redirect("manager_dashboard")
            else:
                return redirect("user_dashboard")
    else:
        form = SignInForm(request)

    return render(request, "signin/signin.html", {"form": form})

@login_required
def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("home")

def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign-in')
        else:
            return HttpResponse("Invalid Id or token")

    except User.DoseNotExist:
        return HttpResponse("User not found")

@user_passes_test(is_admin, login_url="no-permission")
def admin_dashboard(request):
    users = User.objects.prefetch_related("groups").order_by("id")
    groups = Group.objects.prefetch_related("permissions", "user_set").order_by("name")
    return render(
        request,
        "admin/dashboard.html",
        {"users": users, "groups": groups},
    )

@user_passes_test(is_admin, login_url="no-permission")
def assign_role(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data["role"]
            target_user.groups.clear()
            target_user.groups.add(role)
            messages.success(request, f"Role assigned to {target_user.username} successfully")
            return redirect("admin-dashboard")
    else:
        form = AssignRoleForm(initial={"role": target_user.groups.first()})

    return render(
        request,
        "admin/assign_role.html",
        {"form": form, "target_user": target_user},
    )

@user_passes_test(is_admin, login_url="no-permission")
def create_group(request):
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group "{group.name}" created successfully')
            return redirect("admin-dashboard")
    else:
        form = CreateGroupForm()
    return render(request, "admin/create_group.html", {"form": form})