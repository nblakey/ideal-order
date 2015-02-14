from django.conf.urls import patterns, include, url

from orders2.views import create_employee_order

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    (r'^admin/',  include(admin.site.urls)), # admin site
    url(r'^admin/', include(admin.site.urls)),
    url(r'^createemployeeorder/', create_employee_order),
)
    # Examples:
    # url(r'^$', 'idealOrder.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
