from django.contrib import admin

# Register your models here.
from .models import Notification, User

admin.site.register(Notification)
# admin.site.register(User)