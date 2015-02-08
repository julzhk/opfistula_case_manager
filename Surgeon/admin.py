from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from Surgeon.models import Surgeon
from Surgeon.views import SurgeonCreationForm,CREATE_SURGEON_FIELDS

ADMIN_ONLY_FIELDS = ['is_active','is_admin','is_staff','is_superuser']

class SurgeonChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Surgeon
        fields = (
            'first_name',
            'last_name','email',
            'password', 'institution',
            'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class SurgeonAdmin(UserAdmin):
    # The forms to add and change user instances
    form = SurgeonChangeForm
    add_form = SurgeonCreationForm

    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','institution',)}),
        ('Permissions', {'fields': ADMIN_ONLY_FIELDS}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':CREATE_SURGEON_FIELDS + ADMIN_ONLY_FIELDS
        }
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Surgeon, SurgeonAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)