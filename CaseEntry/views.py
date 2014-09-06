from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from CaseEntry.models import CaseForm, CaseFormForm

def case_form(request):
    if request.method == 'POST':
        form = CaseFormForm(request.POST)
        if form.is_valid():
            new_case = form.save()
            return HttpResponseRedirect('/casesubmitted/')
    else:
        form = CaseForm()
    return render(request, 'case_form.html', {'form': form})

def casesubmitted(request):
    return render(request, 'casesubmitted.html')


