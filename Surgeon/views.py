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
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.views.generic.edit import CreateView
from django.forms import ModelForm

def home(request):
    return render(request,
                  'home.html',
        {
            'path':request.META['PATH_INFO']
        }
    )


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

    def get_context_data(self, **kwargs):
        context = super(SurgeonList, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context

class SurgeonDetailView(DetailView):
    model = Surgeon
    queryset = Surgeon.objects.all()

    def get_context_data(self, **kwargs):
        context = super(SurgeonDetailView, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context

class SurgeonForm(ModelForm):
    class Meta:
        model = Surgeon
        fields = ('institution',)

class SurgeonCreate(CreateView):
    model = Surgeon
    fields = ('institution',)

    def post(self, request, *args, **kwargs):
        userform = UserCreationForm(request.POST)
        surgeonform = SurgeonForm(request.POST)
        if userform.is_valid() and surgeonform.is_valid():
            userform.save()
            s = surgeonform.instance
            s.user = userform.instance
            s.save()
            return HttpResponseRedirect('/success/')
        return super(SurgeonCreate, self).post(self,request,*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(SurgeonCreate, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        context['userform'] = UserCreationForm
        return context



class SurgeonUpdate(UpdateView):
    model = Surgeon
    fields = ['institution']
    def get_context_data(self, **kwargs):
        context = super(SurgeonUpdate, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context


class SurgeonDelete(DeleteView):
    model = Surgeon
    success_url = reverse_lazy('surgeon-list')

    def get_context_data(self, **kwargs):
        context = super(SurgeonDelete, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']

        return context
