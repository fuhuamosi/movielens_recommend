# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-14 13:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MovieLens', '0002_auto_20160207_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('movie_tag', models.CharField(max_length=50)),
                ('timestamp', models.IntegerField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MovieLens.Movie')),
            ],
        ),
        migrations.AlterField(
            model_name='rating',
            name='movie_rating',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]