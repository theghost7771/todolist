# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Todo(models.Model):
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    is_done = models.BooleanField(_('Is task done?'))
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo:detail', kwargs={'title': self.title})
