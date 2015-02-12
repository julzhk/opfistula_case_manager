from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.http import Http404
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django import forms
from django.views.generic.edit import CreateView
from django.forms import ModelForm, Form
from django.conf import settings

from Surgeon.models import Surgeon
from Core.models import paginate

from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
CREATE_SURGEON_FIELDS = ['institution', 'partnership_type', 'email', 'first_name', 'last_name',
                         'password1', 'password2']

def home(request):
    return render(request,
                  'home.html', {'path': request.META['PATH_INFO']})


class SurgeonList(ListView):
    model = Surgeon
    context_object_name = 'surgeon_list'
    template_name = 'surgeon/surgeon_list.html'
    paginate_by = settings.PAGE_SIZE

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
        page = self.request.GET.get('page', 1)

        context['surgeon_list'] = paginate(context['surgeon_list'], page)
        return context


class SurgeonDetailView(DetailView):
    model = Surgeon
    queryset = Surgeon.objects.all()
    template_name = 'surgeon/surgeon_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SurgeonDetailView, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context


class SurgeonCreationForm(ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = Surgeon
        fields = CREATE_SURGEON_FIELDS


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(SurgeonCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class SurgeonCreate(CreateView):
    model = Surgeon
    #
    form_class = SurgeonCreationForm
    template_name = 'surgeon/surgeon_form.html'
    def post(self, request, *args, **kwargs):
        userform = SurgeonCreationForm(request.POST)
        if userform.is_valid():
            newuser=userform.save()
            newuser.is_staff= True
            newuser.save()
            messages.add_message(request, messages.INFO, '%s: created!' % newuser.get_full_name())
            return HttpResponseRedirect(reverse_lazy('surgeons'))
        messages.add_message(request, messages.INFO, 'Some error in data')
        return HttpResponseRedirect(reverse_lazy('surgeon_add'))

    def get_context_data(self, **kwargs):
        context = super(SurgeonCreate, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context


class SurgeonUpdate(UpdateView):
    model = Surgeon
    # fields = ['institution']
    # template_name = 'surgeon/surgeon_form.html'

    def get_context_data(self, **kwargs):
        context = super(SurgeonUpdate, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context


class SurgeonDelete(DeleteView):
    model = Surgeon
