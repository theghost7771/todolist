# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.utils.translation import ugettext as _
from django.contrib import messages

from braces.views import LoginRequiredMixin

from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/list.html'
    context_object_name = 'todo_items'


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/detailed.html'


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description']
    success_msg = _('Created')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form.instance.owner = self.request.user
        return super(TodoCreateView, self).form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'is_done']
    success_msg = _('Updated')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form.instance.owner = self.request.user
        return super(TodoUpdateView, self).form_valid(form)
