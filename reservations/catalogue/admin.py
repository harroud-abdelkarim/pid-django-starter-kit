from django.contrib import admin
from .models import Artist
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from catalogue.models import UserMeta

admin.site.register(Artist)


class UserMetaInline(admin.StackedInline):
    model = UserMeta
    can_delete = False
    verbose_name_plural = "user_meta"


class UserAdmin(BaseUserAdmin):
    inlines = [UserMetaInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)