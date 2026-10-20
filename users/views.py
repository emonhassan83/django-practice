from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from users.form import CustomSignUpForm, SignInForm


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
    if request.method == "POST":
        form = SignInForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = SignInForm(request)

    return render(request, "signin/signin.html", {"form": form})


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
    return redirect("home")
