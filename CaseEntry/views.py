from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from CaseEntry.models import PatientRecord, PatientRecordForm, Case, PatientRecordReadOnlyForm
from CaseNotes.models import Note
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from Surgeon.models import Surgeon


@login_required
def case_form(request, id=None):
    this_user = request.user
    form_editable = True
    if request.method == 'POST':
        PatientData = PatientRecordForm(request.POST)
        if PatientData.is_valid():
            new_case = Case()
            new_case.patientrecord = PatientData.save()
            new_case.surgeon = this_user.surgeon
            new_case.save()
            return HttpResponseRedirect('/casesubmitted/')
    else:
        if id:
            PatientData = PatientRecordReadOnlyForm(
                instance=PatientRecord.objects.get(pk=int(id)),
            )
            form_editable = False
        else:
            PatientData = PatientRecordForm()
    return render(request, 'case_form.html', {'form': PatientData,
                                              'form_editable': form_editable,
                                              'user': this_user})


def casesubmitted(request):
    return render(request, 'casesubmitted.html')


class StatusForm(ModelForm):
    class Meta:
        model = Case
        fields = ['status', ]


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['message', ]


def view_case(request, id):
    id = int(id)
    this_user = request.user
    try:
        case = Case.objects.get(id=id)
        if request.method == 'POST':
            NoteData = NoteForm(request.POST)
            StatusData = StatusForm(request.POST)
            if StatusData.is_valid() and this_user.is_superuser:
                case.status = StatusData.cleaned_data['status']
                case.save()
            if NoteData.is_valid():
                new_note = NoteData.save()
                new_note.case = case
                new_note.commenter = this_user
                new_note.save()
        noteform = NoteForm()
        statusform = StatusForm(instance=case)
        return render(request, 'case.html', {'case': case,
                                             'user': this_user,
                                             'noteform': noteform,
                                             'statusform': statusform})
    except Case.DoesNotExist:
        return HttpResponse('case not accessible')


class CaseList(ListView):
    model = Case
    context_object_name = 'cases'
    template_name = 'surgeon_home.html'

    def get_context_data(self, **kwargs):
        # a superuser created in python might not have 1-1 Surgeon model associated
        this_user = self.request.user
        try:
            thissurgeon = this_user.surgeon
        except Surgeon.DoesNotExist:
            this_user.surgeon = Surgeon()
            this_user.surgeon.save()
            this_user.save()
        context = super(CaseList, self).get_context_data(**kwargs)
        context['surgeon'] = self.request.user
        if context['surgeon'].is_superuser:
            context['cases'] = Case.objects.all()
        else:
            context['cases'] = context['surgeon'].surgeon.case_set.all()
        return context