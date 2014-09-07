from django.contrib import admin
from CaseEntry.models import CaseForm, Case
from django import forms
from django.contrib import admin

class CaseAdmin(admin.ModelAdmin):
    def case_name(obj):
        return obj.caseform.patient
    def caseform(obj):
        return "<a href='/admin/CaseEntry/caseform/%s'>Form for %s</a>" % (obj.caseform.id,obj.caseform.patient)
    case_name.short_description = 'Patient'
    caseform.allow_tags= True
    list_filter = ('status',)
    list_display = ( case_name, caseform, 'created_at', 'status',)
    radio_fields = {"status": admin.VERTICAL}

class CaseFormAdmin(admin.ModelAdmin):
    list_display = ( 'patient', 'age', 'surgeon',)

admin.site.register(CaseForm,CaseFormAdmin)
admin.site.register(Case,CaseAdmin)