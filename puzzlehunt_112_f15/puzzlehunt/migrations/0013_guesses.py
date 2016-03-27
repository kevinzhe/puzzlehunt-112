# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0012_auto_20151121_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guesses',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('guess', models.TextField()),
                ('puzzle', models.ForeignKey(to='puzzlehunt.Puzzle')),
                ('team', models.ForeignKey(to='puzzlehunt.Team')),
            ],
        ),
    ]
