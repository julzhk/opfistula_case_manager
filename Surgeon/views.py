from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from CaseEntry.models import PatientRecord, PatientRecordForm, Case
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Surgeon.models import Surgeon


@login_required
def surgeon_home(request):
    # a superuser created in python might not have 1-1 Surgeon model associated
    if request.user.is_authenticated():
        this_user = request.user
        try:
            cases = this_user.surgeon.case_set.all()
        except Surgeon.DoesNotExist:
            this_user.surgeon = Surgeon()
            this_user.surgeon.save()
            this_user.save()
            cases = this_user.surgeon.case_set.all()
        return render(request,
                      'surgeon_home.html',
                      {
                          'cases': cases,
                          'Surgeon': this_user
                      })
    else:
        return HttpResponse('not known')


def home(request):
    return render(request,
                  'home.html',
        {})
