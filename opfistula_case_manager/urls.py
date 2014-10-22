from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from Surgeon.views import SurgeonList, SurgeonDetailView, SurgeonCreate, SurgeonUpdate, SurgeonDelete
from CaseEntry.views import CaseList


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'admin/login.html'}),
                       url(r'^caselist/$', login_required(CaseList.as_view()), name='caselist'),
                       url(r'^submitcase/', 'CaseEntry.views.case_form', name='patientrecord'),
                       url(r'^viewcase/(?P<id>[0-9]+)/$', 'CaseEntry.views.case_form', name='viewpatientrecord'),
                       url(r'^case/(?P<id>[0-9]+)/$', 'CaseEntry.views.view_case', name='case'),
                       url(r'surgeondetails/(?P<pk>[0-9]+)/$', login_required(SurgeonDetailView.as_view()),
                           name='surgeon_details'),
                       url(r'^img/(?P<pk>[0-9]+)', 'CaseEntry.views.serve_img', name='caseimageview'),
                       url(r'^surgeons/$', login_required(SurgeonList.as_view()), name='surgeons'),
                       url(r'^surgeon/add/$', SurgeonCreate.as_view(), name='surgeon_add'),
                       url(r'^surgeon/(?P<pk>[0-9]+)/$', SurgeonUpdate.as_view()),
                       url(r'^surgeon/(?P<pk>[0-9]+)/delete/$', SurgeonDelete.as_view()),

                       url('^register/', login_required(CreateView.as_view(template_name='register.html',
                                                                           form_class=UserCreationForm,
                                                                           success_url='/')), name='register'),
                       url('^accounts/', include('django.contrib.auth.urls')),
                       url(r'^accounts/profile/(?P<pk>\d)/$', login_required(SurgeonDetailView.as_view()),
                           name='profile'),
                       url(r'^$', 'Surgeon.views.home', name='home'),
                       url(r'^admin/', include(admin.site.urls)),
                       )
