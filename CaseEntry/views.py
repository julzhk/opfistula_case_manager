from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from CaseEntry.models import CaseForm

def case_form(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = CaseForm()
    return render(request, 'case_form.html', {'form': form})


