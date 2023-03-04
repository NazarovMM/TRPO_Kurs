from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms.fields import EmailField
from django.forms.forms import Form
from django import forms
from main.models import History

User = get_user_model()


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя', min_length=5, max_length=150)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Повторите пароль', widget=forms.PasswordInput)

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = UserDB.get(username=username)
        if new.count():
            raise ValidationError(
                "Пользователь с таким именем уже зарегистрирован")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = UserDB.get(email=email)
        if new.count():
            raise ValidationError(
                "Пользователь с таким email уже зарегистрирован")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = UserDB(0, self.cleaned_data["username"],
                      self.cleaned_data["email"], self.cleaned_data["password1"])
        user.save()

    @staticmethod
    def is_authenticate(username, password1):
        username1 = UserDB.get(username=username)
        password = UserDB.get(password=password1)
        user = authenticate(username=username1, password=password)
        return user

    def userLogin(self, request, user):
        loginUser = login(request=request, user=user)
        return loginUser




class UserDB(CustomUserCreationForm):

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def save(self, commit=True):
        user = User.objects.create_user(
            self.username, self.email, self.password)
        return user

    def get(self):
        user = User.objects.filter(id=self.id)
        return user

    def update(self):
        user = User.objects.filter(id=self.id).update(
            username=self.username, email=self.email, password=self.password)
        return user

    def delete(self):
        user = User.objects.filter(id=self.id).delete()
        return user

class HistoryDB(History):

    def __init__(self, author, name, date):
        self.id = id
        self.author = author
        self.name = name
        self.date = date

    def create(self, author, name, date, commit=True):
        history = history.objects.create(
            author, name, date)
        return history

    def get(self):
        history = history.objects.filter(id=self.id)
        return history

    def update(self):
        history = history.objects.filter(id=self.id).update(
            author=self.author, name=self.name, date=self.date)
        return history

    def delete(self):
        history = history.objects.filter(id=self.id).delete()
        return history

