# Generated by Django 2.2 on 2019-05-03 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0011_auto_20190501_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automationdata',
            name='isduplicated',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
