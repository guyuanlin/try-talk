# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guest_id', models.CharField(help_text='\u8a66\u7528\u8005 ID', max_length=20, null=True, verbose_name='\u8a66\u7528\u8005 ID', blank=True)),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='\u5efa\u7acb\u6642\u9593')),
                ('user', models.OneToOneField(related_name='guest', null=True, verbose_name='\u4f7f\u7528\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create',),
                'verbose_name': '\u8a66\u7528\u8005',
                'verbose_name_plural': '\u8a66\u7528\u8005',
            },
        ),
    ]
