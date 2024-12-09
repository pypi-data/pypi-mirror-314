from django.contrib import admin
from django.contrib.admin.widgets import AdminTextInputWidget
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, User
from django.db.models import ForeignKey, OneToOneField
from rest_framework.authtoken.models import TokenProxy

from . import models


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
