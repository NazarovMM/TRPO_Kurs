from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class History(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField()
    date = models.TextField()

    @classmethod
    def create(cls, author, name, date):
        History = cls(author=author, name=name, date=date)
        return History
