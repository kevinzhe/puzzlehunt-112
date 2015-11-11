# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0005_auto_20151107_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzleprogress',
            name='team',
            field=models.ForeignKey(related_name='puzzles_started', to='puzzlehunt.Team'),
        ),
    ]
