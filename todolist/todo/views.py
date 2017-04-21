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
    # These next two lines tell the view to index lookups by title
    slug_field = 'title'
    slug_url_kwarg = 'title'


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    fields = ['title', 'description', 'is_done']
    success_msg = _('Created')

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form.instance.owner = self.request.user
        return super(TodoCreateView, self).form_valid(form)
