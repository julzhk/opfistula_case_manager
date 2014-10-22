from django.contrib import admin

from CaseNotes.models import Note


class CaseNotesAdmin(admin.ModelAdmin):
    list_display = ('case', 'message',)


admin.site.register(Note, CaseNotesAdmin)