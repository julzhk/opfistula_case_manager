from django.conf.urls import patterns, include, url
from CaseEntry.views import case_form
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opfistula_case_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^$', 'CaseEntry.views.home', name='home'),
    url(r'^$', 'CaseEntry.views.case_form', name='home'),
    url(r'^case/', 'CaseEntry.views.case_form', name='caseform'),
    url(r'^casesubmitted/', 'CaseEntry.views.casesubmitted', name='casesubmitted'),
    url(r'^admin/', include(admin.site.urls)),
)
