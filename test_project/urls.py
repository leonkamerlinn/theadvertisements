"""test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, re_path
from django.urls import path
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^registration$', views.registration, name='registration'),
    url(r'^activate-email/(?P<token>.+)$', views.activate_email, name='activate_email'),
    url(r'^forgot-password$', views.forgot_password, name='forgot_password'),
    url(r'^reset-password/(?P<token>.+)$', views.reset_password, name='reset_password'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^notes$', views.notes, name='notes'),
    url(r'^notes/(?P<id>[0-9]+)/delete$', views.delete_notes, name='delete_notes'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^groups$', views.groups, name='groups'),
    url(r'^groups/(?P<id>[0-9]+)$', views.group, name='group'),
    url(r'^users$', views.users, name='users'),
    url(r'^users/(?P<id>[0-9]+)$', views.user, name='user'),
    url(r'^users/(?P<id>[0-9]+)/edit$', views.edit_user, name='edit_user'),
    url(r'^users/(?P<id>[0-9]+)/delete$', views.delete_user, name='delete_user'),
    url(r'^users/(?P<id>[0-9]+)/(?P<action>approve|disapprove)$', views.approve_disapprove_user, name='approve_disapprove_user'),
    url(r'^profile$', views.profile, name='profile'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)