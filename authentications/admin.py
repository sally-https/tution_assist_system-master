from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('email', 'username', 'user_type', 'is_superuser', 'is_staff', 'is_active', 'last_login', 'date_joined', 'date_modified')
    list_display_links = ('email', 'username',)
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(User, UserAdmin)