"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

from webparser import views as wp_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', wp_views.index, name='index'),

    url(r'^api/admin', wp_views.admin, name='admin'),

    url("", include('django_socketio.urls')),

] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + [url("", include('django_socketio.urls')),]
