# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0007_auto_20151111_0404'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='curr_puzzle',
            field=models.IntegerField(default=0),
        ),
    ]
