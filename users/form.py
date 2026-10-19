from django import forms
from django.contrib.auth.models import User # Model Used by UserCreationForm and Our new RegistrationForm
from django.contrib.auth.forms import UserCreationForm
from  tasks.forms import StyledFormMixin

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldName in ['username', 'password1', 'password2']:
            self.fields[fieldName].help_text = None

class CustomSignUpForm(StyledFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    # Field level validation Error
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        error = []

        if password and len(password) < 8:
            error.append('Password must be at least 8 characters long')

        if password and not any(char.isdigit() for char in password):
            error.append('Password must contain at least one number')

        if password and not any(char.isalpha() for char in password):
            error.append('Password must contain at least one letter')

        if error:
            raise forms.ValidationError(error)

        return confirm_password

    clean_password2 = clean_confirm_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    # Non field level validation Error
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        error = []

        if password != confirm_password:
            error.append('Passwords do not match')
        
        if error:
            raise forms.ValidationError(error)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    # def __init__(self, *args, **kwargs):
    #     super(CustomSignUpForm, self).__init__(*args, **kwargs)

    #     for fieldName in ['username', 'password1', 'password2']:
    #         self.fields[fieldName].help_text = None