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


class SurgeonForm(ModelForm):
    class Meta:
        model = Surgeon
        fields = ('institution',)


class SurgeonPersonalInfoForm(Form):
    first_name = forms.CharField(label='Surgeon First name', max_length=100)
    last_name = forms.CharField(label='Surgeon First name', max_length=100)
    email = forms.EmailField()


class SurgeonCreate(CreateView):
    model = Surgeon
    template_name = 'surgeon/surgeon_form.html'
    fields = ('institution',)

    def post(self, request, *args, **kwargs):
        userform = UserCreationForm(request.POST)
        surgeonform = SurgeonForm(request.POST)
        personal_info = SurgeonPersonalInfoForm(request.POST)
        if userform.is_valid() and surgeonform.is_valid() and personal_info.is_valid():
            userform.save()
            s = surgeonform.instance
            s.user = userform.instance
            for i in personal_info.cleaned_data:
                s.user.__setattr__(i, personal_info.cleaned_data[i])
            s.user.is_staff = True
            s.user.save()
            s.save()
            messages.add_message(request, messages.INFO, '%s: created!' % s.user.username)
            return HttpResponseRedirect(reverse_lazy('surgeons'))
        messages.add_message(request, messages.INFO, 'Some error in data')
        return HttpResponseRedirect(reverse_lazy('surgeon_add'))

    def get_context_data(self, **kwargs):
        context = super(SurgeonCreate, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        context['userform'] = UserCreationForm(initial={'username': 'name'})
        context['personalinfoform'] = SurgeonPersonalInfoForm()
        return context


class SurgeonUpdate(UpdateView):
    model = Surgeon
    fields = ['institution']
    template_name = 'surgeon/surgeon_form.html'

    def get_context_data(self, **kwargs):
        context = super(SurgeonUpdate, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']
        return context


class SurgeonDelete(DeleteView):
    model = Surgeon
    template_name = 'surgeon/surgeon_form.html'
    success_url = reverse_lazy('surgeon-list')

    def get_context_data(self, **kwargs):
        context = super(SurgeonDelete, self).get_context_data(**kwargs)
        context['path'] = self.request.META['PATH_INFO']

        return context
