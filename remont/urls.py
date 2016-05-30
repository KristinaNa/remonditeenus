# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf.urls import url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.views.generic import TemplateView

from remonditeenus import settings
from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^add/$', views.Add_new_device.as_view()),
    url(r'^order/$', views.Order.as_view()),

    url(r'^service_order/$', views.Service_order.as_view()),


    url(r'^lisa_service_device/$', views.lisa_service_device, name='lisa_service_device'),


    url(r'^remont/remontservice/(?P<device_id>\d+)$', views.get_json),
    url(r'^note/(?P<id>\d+)$', views.get_note_json),
    url(r'^note/(?P<id>\d+/new)$', views.save_note),


    url(r'^seadme_otsing/$', views.server_list, name='seadme_otsing'),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
    #url(r'^$', TemplateView.as_view(template_name='lisa_uus_seade.html'), name='main'),


    url(r'^service_action/$', views.service_action, name='service_action'),
    url(r'^service_device/$', views.service_device, name='service_action'),
]