from django.conf.urls import patterns, include, url
from CaseEntry.views import case_form
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'opfistula_case_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^case/', 'CaseEntry.views.case_form', name='name'),
    url(r'^admin/', include(admin.site.urls)),
)
