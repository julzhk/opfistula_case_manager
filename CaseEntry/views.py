from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from CaseEntry.models import PatientRecord, PatientRecordForm, Case
from django.contrib.auth.decorators import login_required


@login_required
def case_form(request):
    this_user = request.user
    if request.method == 'POST':
        # save the form data
        PatientData = PatientRecordForm(request.POST)
        if PatientData.is_valid():
            new_case = Case()
            new_case.patientrecord = PatientData.save()
            new_case.surgeon = this_user.surgeon
            new_case.save()
            return HttpResponseRedirect('/casesubmitted/')
    else:
        PatientData = PatientRecordForm()
    return render(request, 'case_form.html', {'form': PatientData,
                                              'user': this_user})

def casesubmitted(request):
    return render(request, 'casesubmitted.html')

def view_case(request, id):
    id = int(id)
    case = Case.objects.get(id=id)
    return HttpResponse(str(case))

