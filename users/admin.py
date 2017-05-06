from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User


# Deactivate the unused built-in Group admin
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ['username']
    list_filter = []
    search_fields = ['username']
