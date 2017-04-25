# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.utils.translation import ugettext as _
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin

from .models import Todo


class TodoActionMixin(object):
    model = Todo
    success_url = reverse_lazy('todo:home')

    @property
    def success_msg(self):
        return NotImplemented

    def get_object(self, queryset=None):
        obj = super(TodoActionMixin, self).get_object()
        if obj.owner.id != self.request.user.id:
            raise Http404
        return obj

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        form.instance.owner = self.request.user
        return super(TodoActionMixin, self).form_valid(form)


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/list.html'
    context_object_name = 'todo_items'

    def get_queryset(self):
        return Todo.objects.select_related()


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/detailed.html'


class TodoCreateView(LoginRequiredMixin, TodoActionMixin, CreateView):
    fields = ['title', 'description']
    success_msg = _('Created')


class TodoUpdateView(LoginRequiredMixin, TodoActionMixin, UpdateView):
    fields = ['title', 'description', 'is_done']
    success_msg = _('Updated')


class TodoDeleteView(LoginRequiredMixin, TodoActionMixin, DeleteView):
    template_name = 'todo/delete.html'
    success_msg = _('Deleted')
