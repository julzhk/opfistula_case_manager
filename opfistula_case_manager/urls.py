from django.conf.urls import patterns, include, url
from CaseEntry.views import case_form
from django.contrib import admin
from Surgeon.views import SurgeonList, SurgeonDetailView, SurgeonCreate, SurgeonUpdate, SurgeonDelete
from CaseEntry.views import CaseList


admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'opfistula_case_manager.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # url(r'^$', 'CaseEntry.views.home', name='home'),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'admin/login.html'}),
                       url(r'^caselist/$', CaseList.as_view(), name='caselist'),
                       url(r'^submitcase/', 'CaseEntry.views.case_form', name='patientrecord'),
                       url(r'^viewcase/(?P<id>\d)/$', 'CaseEntry.views.case_form', name='viewpatientrecord'),
                       url(r'^case/(?P<id>\d)/$', 'CaseEntry.views.view_case', name='case'),
                       url(r'^casesubmitted/', 'CaseEntry.views.casesubmitted', name='casesubmitted'),

                       url(r'^surgeondetails/(?P<pk>\d)/$', SurgeonDetailView.as_view(), name='surgeon_details'),

                       url(r'^surgeons/$', SurgeonList.as_view(), name='surgeons'),
                       # url(r'surgeon/add/$', SurgeonCreate.as_view(), name='surgeon_add'),
                       # url(r'surgeon/(?P<pk>[0-9]+)/$', SurgeonUpdate.as_view() ),
                       # url(r'surgeon/(?P<pk>[0-9]+)/delete/$', SurgeonDelete.as_view()),

                       url(r'^$', 'Surgeon.views.home', name='home'),
                       url(r'^admin/', include(admin.site.urls)),

)
