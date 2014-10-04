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
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy


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


class SurgeonCreate(CreateView):
    model = Surgeon
    fields = '__all__'


class SurgeonUpdate(UpdateView):
    model = Surgeon
    fields = ['institution']


class SurgeonDelete(DeleteView):
    model = Surgeon
    success_url = reverse_lazy('surgeon-list')