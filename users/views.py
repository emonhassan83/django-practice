from django.shortcuts import render, redirect
from django.contrib.auth.models import User # Model Used by UserCreationForm and Our new RegistrationForm
from django.contrib.auth.forms import UserCreationForm # Built-in Form for Registering a New User
from .form import SignUpForm, CustomSignUpForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def sign_up(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sign-in')
    else:
        form = CustomSignUpForm()

    return render(request, 'signup/signup.html', {'form': form})


def sign_in(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid username or password. Please try again."

    return render(request, 'signin/signin.html', {'error': error})

def sign_out(request):
    logout(request)
    return redirect('home')
