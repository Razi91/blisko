from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from web import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main),
    url(r'^tests/', views.tests),
    url(r'^kursy/$', views.kursy),
    url(r'^kurs/([0-9]+)/', views.kurs),
    url(r'^test/([0-9]+)/', views.test),
    url(r'^lekcja/([0-9]+)/', views.lekcja)
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
