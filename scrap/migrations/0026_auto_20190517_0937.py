# Generated by Django 2.2 on 2019-05-17 09:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0025_auto_20190517_0937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationdata',
            name='entry_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2019, 5, 17, 9, 37, 28, 230914)),
        ),
    ]
