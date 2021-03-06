# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.TodoListView.as_view(), name='home'),
    url(
        regex=r'^add$',
        view=views.TodoCreateView.as_view(),
        name='create'
    ),
    url(
        regex=r'^todo/(?P<pk>\d+)/edit$',
        view=views.TodoUpdateView.as_view(),
        name='edit'
    ),
    url(
        regex=r'^todo/(?P<pk>\d+)/delete$',
        view=views.TodoDeleteView.as_view(),
        name='delete'
    ),
    url(
        regex=r'^todo/mark_done$',
        view=views.TodoMarkDoneView.as_view(),
        name='mark_done'
    ),
]
