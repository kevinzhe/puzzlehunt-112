# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0004_auto_20151107_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teammember',
            name='team',
            field=models.ForeignKey(related_name='members', blank=True, to='puzzlehunt.Team', null=True),
        ),
    ]
