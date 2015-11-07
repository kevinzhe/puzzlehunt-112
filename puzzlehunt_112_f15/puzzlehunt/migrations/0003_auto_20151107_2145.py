# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0002_puzzle_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(related_name='members', to='puzzlehunt.Team'),
        ),
    ]
