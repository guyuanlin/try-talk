# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter_accounts', '0003_auto_20150711_1137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='twitterid',
            options={'ordering': ('-create',), 'verbose_name': 'Twitter \u4f7f\u7528\u8005', 'verbose_name_plural': 'Twitter \u4f7f\u7528\u8005'},
        ),
    ]
