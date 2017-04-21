# -*- coding: utf-8 -*-

from django.db import models


class Todo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
