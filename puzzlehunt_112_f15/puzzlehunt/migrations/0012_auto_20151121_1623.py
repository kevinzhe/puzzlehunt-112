# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzlehunt', '0011_auto_20151118_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='passcode',
            field=models.CharField(default='abc', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hint',
            name='time_shown',
            field=models.DurationField(help_text='hh:mm:ss'),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='time_limit',
            field=models.DurationField(help_text='hh:mm:ss'),
        ),
    ]
