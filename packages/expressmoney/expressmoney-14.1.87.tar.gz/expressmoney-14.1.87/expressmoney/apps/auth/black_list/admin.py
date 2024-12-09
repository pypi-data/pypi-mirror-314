from django.contrib import admin

from .models import BlackList, WhiteList


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_id', 'passport_serial', 'passport_number', 'cause', 'comment')
    search_fields = ('=user_id', '=passport_number')
    list_filter = ('cause',)
    ordering = ('-created', )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WhiteList)
class WhiteListListAdmin(admin.ModelAdmin):
    list_display = ('created', 'user_id', 'comment')
    search_fields = ('=user_id',)
    ordering = ('-created',)
