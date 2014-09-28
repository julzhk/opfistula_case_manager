from django.contrib import admin
from CaseEntry.models import PatientRecord, Case, CASE_STATUS_CHOICES
from django import forms
from django.contrib import admin
from CaseNotes.models import Note


class CaseNotesInline(admin.TabularInline):
    model = Note
    can_delete = False


class CaseAdminForm(forms.ModelForm):
    def clean_status(self):
        status_incremental_codes = {cc[0]: i for (i, cc) in enumerate(CASE_STATUS_CHOICES)}

        if status_incremental_codes[self.initial['status']] > \
                status_incremental_codes[self.cleaned_data['status']]:
            raise forms.ValidationError('Cannot move status backwards')
        return self.cleaned_data["status"]


class CaseAdmin(admin.ModelAdmin):
    def case_name(obj):
        return obj.patientrecord.patient

    def patientrecord(obj):
        return "<a href='/admin/CaseEntry/patientrecord/%s'>Form for %s</a>" % (
        obj.patientrecord.id, obj.patientrecord.patient)

    case_name.short_description = 'Patient'
    patientrecord.allow_tags = True
    list_filter = ('status',)
    list_display = ( case_name, patientrecord, 'created_at', 'status',)
    radio_fields = {"status": admin.VERTICAL}
    inlines = [CaseNotesInline, ]
    form = CaseAdminForm


class PatientRecordAdmin(admin.ModelAdmin):
    list_display = ( 'patient', 'age',)


admin.site.register(PatientRecord, PatientRecordAdmin)
admin.site.register(Case,CaseAdmin)