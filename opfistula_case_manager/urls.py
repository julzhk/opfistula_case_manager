from django.conf.urls import patterns, include, url
from CaseEntry.views import case_form
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'opfistula_case_manager.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       # url(r'^$', 'CaseEntry.views.home', name='home'),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
                       url(r'^accounts/login/$', 'django.contrib.auth.views.login',
                           {'template_name': 'admin/login.html'}),
                       url(r'^caselist/$', 'Surgeon.views.surgeon_home', name='caselist'),
                       url(r'^submitcase/', 'CaseEntry.views.case_form', name='patientrecord'),
                       url(r'^viewcase/(?P<id>\d)/$', 'CaseEntry.views.case_form', name='viewpatientrecord'),
                       url(r'^case/(?P<id>\d)/$', 'CaseEntry.views.view_case', name='case'),
                       url(r'^casesubmitted/', 'CaseEntry.views.casesubmitted', name='casesubmitted'),
                       url(r'^$', 'Surgeon.views.home', name='home'),
                       url(r'^admin/', include(admin.site.urls)),

)
