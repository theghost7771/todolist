# -*- coding: utf-8 -*-

from django.views.generic import ListView, UpdateView, CreateView

from braces.views import LoginRequiredMixin

from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/list.html'
