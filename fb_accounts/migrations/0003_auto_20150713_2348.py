# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fb_accounts', '0002_auto_20150711_1136'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facebookid',
            options={'ordering': ('-create',), 'verbose_name': 'Facebook \u4f7f\u7528\u8005', 'verbose_name_plural': 'Facebook \u4f7f\u7528\u8005'},
        ),
    ]
