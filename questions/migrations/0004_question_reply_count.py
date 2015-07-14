# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20150714_2239'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='reply_count',
            field=models.IntegerField(default=0, verbose_name='\u56de\u8986\u6578'),
        ),
    ]
