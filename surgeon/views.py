from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from CaseEntry.models import CaseForm, CaseFormForm, Case
from django.contrib.auth.decorators import login_required


@login_required
def surgeon_home(request):
    if request.user.is_authenticated():
        this_user = request.user
        cases = this_user.surgeon.case_set.all()
        return render(request,
                      'surgeon_home.html',
                      {
                        'cases': cases,
                        'surgeon':this_user
                      })
    else:
        return HttpResponse('not known')

