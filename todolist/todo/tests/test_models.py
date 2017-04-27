# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Todo


class MyTestCase(TestCase):

    def test_mark_done(self):
        user = User.objects.create_user(email='user@…', username='user', password='somepasswd')
        todo = Todo(title='SomeTitle', description='SomeDescr', owner=user)
        res = todo.mark_done(user)
        self.assertTrue(res)
        self.assertEqual(Todo.objects.count(), 1)

    def test_mark_done_already_done(self):
        user = User.objects.create_user(email='user@…', username='user', password='somepasswd')
        todo = Todo(title='SomeTitle', description='SomeDescr', is_done=True, done_by=user, owner=user)
        res = todo.mark_done(user)
        self.assertIsNone(res)
        # todo not saved because mark_done don't save already done todos
        self.assertEqual(Todo.objects.count(), 0)
