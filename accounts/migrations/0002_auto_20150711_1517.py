# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='guest_id',
            field=models.CharField(null=True, max_length=20, blank=True, help_text='\u8a66\u7528\u8005 ID', unique=True, verbose_name='\u8a66\u7528\u8005 ID'),
        ),
    ]
