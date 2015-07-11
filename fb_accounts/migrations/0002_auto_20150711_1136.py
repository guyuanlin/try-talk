# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fb_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facebookid',
            options={'ordering': ('-create',), 'verbose_name': 'Facebook ID', 'verbose_name_plural': 'Facebook IDs'},
        ),
        migrations.AddField(
            model_name='facebookid',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 11, 3, 36, 11, 788559, tzinfo=utc), verbose_name='\u5efa\u7acb\u6642\u9593', auto_now_add=True),
            preserve_default=False,
        ),
    ]
