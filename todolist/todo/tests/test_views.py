# -*- coding: utf-8 -*-

from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from django.http import Http404

from ..views import TodoCreateView
from ..models import Todo


class MyTestCase(TestCase):

    def setUp(self):
        self.credentials = {'username': 'user', 'password': 'qweasd'}
        self.user = User.objects.create_user(email='user@…', **self.credentials)
        self.client = Client()
        self.client.login(**self.credentials)


class TestTodoCreateView(MyTestCase):

    def test_get(self):
        request = RequestFactory().get(reverse('todo:create'))

        request.user = self.user

        response = TodoCreateView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_get_anonymous(self):
        request = RequestFactory().get(reverse('todo:create'))

        request.user = AnonymousUser()

        response = TodoCreateView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/add')

    def test_post(self):
        response = self.client.post(reverse('todo:create'),
                                    {'title': 'Some title', 'description': 'some description'},
                                    follow=True)

        # assert client was redirected, and page contains our task
        self.assertRedirects(response, reverse('todo:home'), status_code=302, target_status_code=200)
        self.assertContains(response, 'Some title')
        self.assertContains(response, 'some description')
        self.assertEqual(Todo.objects.count(), 1)


class TestTodoUpdateView(MyTestCase):

    def test_get_not_existing(self):
        response = self.client.get(reverse('todo:edit', args=[5000]))
        # check 404 for not existing Todo
        self.assertEqual(response.status_code, 404)

    def test_get_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('todo:edit', args=[5000]))
        self.assertRedirects(response,
                             '{}?next=/todo/5000/edit'.format(reverse('login')),
                             status_code=302,
                             target_status_code=200)

    def test_get_existing(self):
        todo = Todo(title='Todo for edit',
                    description='This is to do for editing',
                    owner=self.user)
        todo.save()
        response = self.client.get(reverse('todo:edit', args=[todo.id]))
        self.assertContains(response, todo.title)
        self.assertContains(response, todo.description)

    def test_another_user_trying_to_get_edit(self):
        """Here we create task for user2, and try to get edit page by user, 403 should be raised"""
        another_user = User.objects.create_user(email='user2@…', username='user2', password='user2pass')

        todo = Todo(title='a', description='b', owner=another_user)
        todo.save()

        response = self.client.get(reverse('todo:edit', args=[todo.id]))
        self.assertEqual(response.status_code, 403)

    def test_post(self):
        todo = Todo(title='SomeTitle', description='SomeDescription', owner=self.user)
        todo.save()

        response = self.client.post(reverse('todo:edit', args=[todo.id]),
                                    {'title': 'ChangedTitle', 'description': 'ChangedDescription'})
        self.assertRedirects(response, reverse('todo:home'), status_code=302, target_status_code=200)
        # load new data from db
        todo.refresh_from_db()
        self.assertEqual(todo.title, 'ChangedTitle')
        self.assertEqual(todo.description, 'ChangedDescription')


class TestTodoListView(MyTestCase):

    def test_get_anonymous(self):
        self.client.logout()
        response = self.client.get(reverse('todo:home'))
        self.assertRedirects(response,
                             '{}?next=/'.format(reverse('login')),
                             status_code=302,
                             target_status_code=200)

    def test_get_empty(self):
        response = self.client.get(reverse('todo:home'))
        self.assertContains(response, 'Sorry, no ToDo\'s here')

    def test_get(self):
        session = self.client.session
        todos = [
            Todo(title='ToDoOne', description='DescriptionOne', owner=self.user, is_done=True),
            Todo(title='ToDoTwo', description='DescriptionTwo', owner=self.user),
            Todo(title='ToDoThree', description='DescriptionThree', owner=self.user, is_done=True)
        ]
        Todo.objects.bulk_create(todos)

        response = self.client.get(reverse('todo:home'))
        for todo in todos:
            self.assertContains(response, todo.title)

        session['hide_done'] = 'True'
        session.save()
        response = self.client.get(reverse('todo:home'))

        self.assertContains(response, 'ToDoTwo')
        self.assertNotContains(response, 'ToDoOne')
        self.assertNotContains(response, 'ToDoThree')

    def test_session_hide_done_change(self):
        # ensure is None by default
        response = self.client.get(reverse('todo:home'))
        self.assertIsNone(self.client.session.get('hide_done'))

        response = self.client.get('{}?hide_done=True'.format(reverse('todo:home')))
        self.assertTrue(self.client.session['hide_done'])

        response = self.client.get('{}?hide_done=False'.format(reverse('todo:home')))
        self.assertFalse(self.client.session['hide_done'])


class TestTodoMarkDoneView(MyTestCase):

    def test_anonymous(self):
        todo = Todo(title='SomeTitle', description='SomeDescription', owner=self.user)
        todo.save()
        response = self.client.post(reverse('todo:mark_done'), {'id': todo.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertDictEqual(response.json(), {'is_done': True, 'done_by': str(self.user)})

        another_user = User.objects.create_user(email='user2@…', username='user2', password='user2pass')
        todo.refresh_from_db()
        todo.done_by = another_user
        todo.save()
        # trying to mark_done already done task, and it's done by another user
        response = self.client.post(reverse('todo:mark_done'), {'id': todo.id}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertDictEqual(response.json(), {'is_done': None, 'done_by': str(another_user)})
