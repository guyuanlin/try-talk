# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_accounts', '0002_auto_20150710_1916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='twitterid',
            options={'ordering': ('-create',), 'verbose_name': 'Twitter ID', 'verbose_name_plural': 'Twitter IDs'},
        ),
        migrations.AddField(
            model_name='twitterid',
            name='create',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 11, 3, 37, 2, 374270, tzinfo=utc), verbose_name='\u5efa\u7acb\u6642\u9593', auto_now_add=True),
            preserve_default=False,
        ),
    ]
