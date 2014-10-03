from django.shortcuts import render
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from CaseEntry.models import PatientRecord, PatientRecordForm, Case
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Surgeon.models import Surgeon
from django.views.generic import ListView
from django.http import Http404
from django.views.generic import DetailView
from django.utils import timezone

@login_required
def surgeon_home(request):
    # a superuser created in python might not have 1-1 Surgeon model associated
    if request.user.is_authenticated():
        this_user = request.user
        try:
            thissurgeon = this_user.surgeon
        except Surgeon.DoesNotExist:
            this_user.surgeon = Surgeon()
            this_user.surgeon.save()
            this_user.save()
        # staff see every case; surgeons, just their own
        if this_user.is_staff or this_user.is_superuser:
            cases = Case.objects.all()
        else:
            cases = this_user.surgeon.case_set.all()
        return render(request,
                      'surgeon_home.html',
                      {
                          'user': this_user,
                          'cases': cases,
                          'Surgeon': this_user
                      })
    else:
        return HttpResponse('not known')


def surgeon_details(request,id):
    return render(request,
                  'home.html',
        {})

def home(request):
    return render(request,
                  'home.html',
        {})

class SurgeonList(ListView):
    model = Surgeon
    context_object_name = 'surgeon_list'
    def get_queryset(self):
        qs = self.model.objects.all()
        this_user = self.request.user
        if not this_user.is_superuser:
            raise Http404()
        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(user__username__icontains=search)
        return qs

class SurgeonDetailView(DetailView):
    model = Surgeon
    queryset = Surgeon.objects.all()
