# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0005_auto_20150715_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLocationHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(help_text='\u66fe\u7d93\u53d6\u5f97\u554f\u984c\u5217\u8868\u6216\u767c\u554f\u7684\u4f4d\u7f6e', srid=4326, verbose_name='\u4f4d\u7f6e')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='\u5efa\u7acb\u6642\u9593')),
                ('user', models.ForeignKey(verbose_name='\u4f7f\u7528\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create',),
                'verbose_name': '\u4f7f\u7528\u8005\u4f4d\u7f6e\u6b77\u53f2\u7d00\u9304',
                'verbose_name_plural': '\u4f7f\u7528\u8005\u4f4d\u7f6e\u6b77\u53f2\u7d00\u9304',
            },
        ),
        migrations.AddField(
            model_name='reply',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=None, help_text='\u56de\u7b54\u4f4d\u7f6e', srid=4326, null=True, verbose_name='\u56de\u7b54\u4f4d\u7f6e'),
        ),
    ]
