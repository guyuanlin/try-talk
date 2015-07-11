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
            name='FacebookID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fb_id', models.CharField(help_text='\u4f7f\u7528\u8005\u7684 FB ID', max_length=200, verbose_name='\u4f7f\u7528\u8005\u7684 FB ID')),
                ('user', models.OneToOneField(verbose_name='\u4f7f\u7528\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Facebook ID',
                'verbose_name_plural': 'Facebook IDs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='facebookid',
            unique_together=set([('fb_id',)]),
        ),
    ]
