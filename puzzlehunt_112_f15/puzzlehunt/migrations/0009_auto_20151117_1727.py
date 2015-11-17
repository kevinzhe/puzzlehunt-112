# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0008_team_curr_puzzle'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='passcode',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='solution',
            field=models.TextField(),
        ),
    ]
