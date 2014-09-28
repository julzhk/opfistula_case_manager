from django.contrib import admin
from CaseNotes.models import Note
from django import forms
from django.contrib import admin


class CaseNotesAdmin(admin.ModelAdmin):
    list_display = ( 'case', 'message',)


admin.site.register(Note, CaseNotesAdmin)