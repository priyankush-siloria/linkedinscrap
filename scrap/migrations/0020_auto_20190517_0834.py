# Generated by Django 2.2 on 2019-05-17 08:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0019_auto_20190517_0829'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationdata',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2019, 5, 17, 8, 34, 24, 738628), null=True),
        ),
    ]
