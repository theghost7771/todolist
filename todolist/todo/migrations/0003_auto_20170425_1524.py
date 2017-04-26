# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-25 15:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0002_auto_20170421_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='done_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='done_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='todo',
            name='is_done',
            field=models.BooleanField(default=False, verbose_name='Is task done?'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
