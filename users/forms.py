from django import forms
from django.contrib.auth.models import User
from django.forms import ValidationError


# Form for validate a signin user
class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label="Password Confirm")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                "A user with this username is already exists. Please choose a different one."
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "A user with this email is already exists. Please choose a different one."
            )
        return email

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("password don't match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# Form for validate a login user
class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
