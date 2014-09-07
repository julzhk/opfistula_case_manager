from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from CaseEntry.models import CaseForm, CaseFormForm, Case

def case_form(request):
    if request.method == 'POST':
        form = CaseFormForm(request.POST)
        if form.is_valid():
            new_caseform = form.save()
            new_case = Case()
            new_case.caseform = new_caseform
            new_case.save()

            return HttpResponseRedirect('/casesubmitted/')
    else:
        form = CaseFormForm()
    return render(request, 'case_form.html', {'form': form})

def casesubmitted(request):
    return render(request, 'casesubmitted.html')


