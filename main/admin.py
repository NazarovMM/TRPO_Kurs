from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import History

admin.site.register(History)

User = get_user_model()

@admin.register(User)
class UserAdmin(UserAdmin):
    pass