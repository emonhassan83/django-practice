from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from tasks.forms import StyledFormMixin


class CustomSignUpForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "confirm_password"]

    def clean_password(self):
        password = self.cleaned_data.get("password")
        errors = []

        if password and len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        if password and not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one number")
        if password and not any(char.isalpha() for char in password):
            errors.append("Password must contain at least one letter")

        if errors:
            raise forms.ValidationError(errors)
        return password

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class SignInForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
