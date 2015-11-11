# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0006_auto_20151111_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hint',
            name='puzzle',
            field=models.ForeignKey(related_name='hints', to='puzzlehunt.Puzzle'),
        ),
    ]
