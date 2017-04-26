# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, View
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.urls import reverse_lazy

from braces.views import LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin

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
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        form.instance.owner = self.request.user
        return super(TodoActionMixin, self).form_valid(form)


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo/detailed.html'


class TodoCreateView(LoginRequiredMixin, TodoActionMixin, CreateView):
    fields = ['title', 'description']
    success_msg = _('Task created')


class TodoUpdateView(LoginRequiredMixin, TodoActionMixin, UpdateView):
    fields = ['title', 'description', 'is_done']
    success_msg = _('Task updated')


class TodoDeleteView(LoginRequiredMixin, TodoActionMixin, DeleteView):
    template_name = 'todo/delete.html'
    success_msg = _('Task deleted')


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo/list.html'
    context_object_name = 'todo_items'
    paginate_by = 20

    def get_queryset(self):
        # to prevent multiple request to users table add select_related here
        queryset = Todo.objects.select_related('owner', 'done_by')

        # save state to session
        if 'hide_done' in self.request.GET:
            self.request.session['hide_done'] = self.request.GET['hide_done']
            self.request.session.modified = True

        # modify queryset according to user wishes
        if self.request.session.get('hide_done') == 'True':
            queryset = queryset.filter(is_done=False)

        return queryset


class TodoStatusSwitchView(LoginRequiredMixin, JSONResponseMixin, AjaxResponseMixin, View):

    def post_ajax(self, request, *args, **kwargs):
        todo = Todo.objects.get(id=request.POST.get('id'))
        result = todo.mark_done(request.user)
        return self.render_json_response({'is_done': result, 'done_by': str(todo.done_by)})
