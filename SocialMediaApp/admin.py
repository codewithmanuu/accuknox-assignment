from django.contrib import admin
from .models import Useraccount, FriendRequest
# Register your models here.
admin.site.register([Useraccount, FriendRequest])