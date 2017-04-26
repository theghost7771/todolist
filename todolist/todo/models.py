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
    is_done = models.BooleanField(_('Is task done?'), default=False)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='owner')
    done_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, related_name='done_by')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('todo:detail', args=[self.id])

    def mark_done(self, user):
        """Mark task as done, record who did it, and save row"""
        if not self.is_done:
            self.is_done = True
            self.done_by = user
            self.save()
            return True
