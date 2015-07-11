# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('twitter_accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('twitter_id', models.CharField(help_text='\u4f7f\u7528\u8005\u7684 Twitter ID', unique=True, max_length=200, verbose_name='\u4f7f\u7528\u8005\u7684 Twitter ID')),
                ('user', models.OneToOneField(verbose_name='\u4f7f\u7528\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Twitter ID',
                'verbose_name_plural': 'Twitter IDs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='facebookid',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='facebookid',
            name='user',
        ),
        migrations.DeleteModel(
            name='FacebookID',
        ),
    ]
