from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from surgeon.models import Surgeon


class SurgeonInline(admin.StackedInline):
    model = Surgeon
    can_delete = False
    verbose_name_plural = 'surgeon'


class UserAdmin(UserAdmin):
    inlines = (SurgeonInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)