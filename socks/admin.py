from django.contrib import admin

from .models import Sock, SockMatch


@admin.register(Sock)
class SockAdmin(admin.ModelAdmin):

    list_display = ['owner', 'name']
    list_filter = ['owner', 'size_description', 'is_rental']
    search_fields = ['name', 'user__username']


@admin.register(SockMatch)
class SockMatchAdmin(admin.ModelAdmin):

    list_display = ['sock1', 'sock2', 'winner']
