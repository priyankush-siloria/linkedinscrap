# Generated by Django 2.2 on 2019-05-27 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0040_scriptinterval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptinterval',
            name='interval',
            field=models.DateTimeField(blank=True, default='', null=True),
        ),
    ]
