# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': '\u95dc\u9375\u5b57', 'verbose_name_plural': '\u95dc\u9375\u5b57'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u95dc\u9375\u5b57'),
        ),
    ]
