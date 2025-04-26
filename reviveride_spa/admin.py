from django.contrib import admin

# Register your models here.
from .models import Notification, User, ContactMessage

admin.site.register(Notification)
admin.site.register(ContactMessage)
# admin.site.register(User)