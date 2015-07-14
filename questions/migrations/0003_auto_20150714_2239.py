# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_auto_20150714_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(max_length=30, verbose_name='\u5206\u985e', choices=[(b'food', b'food'), (b'shop', b'shop'), (b'location', b'location'), (b'other', b'other')]),
        ),
    ]
