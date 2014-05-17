from django.conf.urls import patterns, include, url

from django.contrib import admin

from web import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main),
    url(r'^tests/', views.tests),
    url(r'^test/(+d)', views.test)
)
