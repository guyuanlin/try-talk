# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.CharField(max_length=30, verbose_name='\u5206\u985e', choices=[(b'food', b'food'), (b'service', b'service'), (b'navigation', b'navigation'), (b'others', b'others')])),
                ('content', models.TextField(verbose_name='\u5167\u5bb9', validators=[django.core.validators.MaxLengthValidator(500)])),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='\u767c\u554f\u4f4d\u7f6e')),
                ('is_active', models.BooleanField(default=True, verbose_name='\u6709\u6548')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='\u5efa\u7acb\u6642\u9593')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u6642\u9593')),
                ('owner', models.ForeignKey(verbose_name='\u767c\u554f\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-create',),
                'verbose_name': '\u554f\u984c\u5217\u8868',
                'verbose_name_plural': '\u554f\u984c\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='\u5167\u5bb9', validators=[django.core.validators.MaxLengthValidator(500)])),
                ('is_active', models.BooleanField(default=True, verbose_name='\u6709\u6548')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='\u5efa\u7acb\u6642\u9593')),
                ('update', models.DateTimeField(auto_now=True, verbose_name='\u66f4\u65b0\u6642\u9593')),
                ('likes', models.ManyToManyField(related_name='like_replys', verbose_name='\u6309\u8b9a\u4f7f\u7528\u8005', to=settings.AUTH_USER_MODEL)),
                ('question', models.ForeignKey(related_name='replys', verbose_name='\u6240\u5c6c\u554f\u984c', to='questions.Question')),
                ('user', models.ForeignKey(verbose_name='\u56de\u8986\u8005', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u554f\u984c\u56de\u8986',
                'verbose_name_plural': '\u554f\u984c\u56de\u8986',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u6a19\u7c64\u540d\u7a31')),
            ],
            options={
                'verbose_name': '\u6a19\u7c64',
                'verbose_name_plural': '\u6a19\u7c64',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='questions.Tag', verbose_name='\u6a19\u7c64'),
        ),
    ]
