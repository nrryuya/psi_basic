# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-16 03:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='amazon_category',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='amazon_url',
            field=models.TextField(),
        ),
    ]
