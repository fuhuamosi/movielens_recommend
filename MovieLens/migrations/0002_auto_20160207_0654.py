# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-07 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MovieLens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='timestamp',
            field=models.IntegerField(),
        ),
    ]