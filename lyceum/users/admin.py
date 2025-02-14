from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from users.models import Profile

__all__ = []


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    readonly_fields = (Profile.display_image_300x300,)


class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
