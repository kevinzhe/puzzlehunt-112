# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0009_auto_20151117_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValidUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('andrew_id', models.CharField(max_length=50)),
                ('role', models.CharField(choices=[('student', 'Student'), ('author', 'Author')], max_length=50, default='student')),
            ],
        ),
    ]
