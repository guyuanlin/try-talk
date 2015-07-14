# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_question_reply_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(help_text='\u554f\u984c\u5206\u985e', max_length=30, verbose_name='\u5206\u985e', choices=[(b'food', b'food'), (b'shop', b'shop'), (b'location', b'location'), (b'other', b'other')]),
        ),
        migrations.AlterField(
            model_name='question',
            name='content',
            field=models.TextField(help_text='\u5167\u5bb9', verbose_name='\u5167\u5bb9', validators=[django.core.validators.MaxLengthValidator(500)]),
        ),
        migrations.AlterField(
            model_name='question',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(help_text='\u767c\u554f\u4f4d\u7f6e', srid=4326, verbose_name='\u767c\u554f\u4f4d\u7f6e'),
        ),
    ]
