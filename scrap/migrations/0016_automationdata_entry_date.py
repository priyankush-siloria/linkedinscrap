# Generated by Django 2.2 on 2019-05-17 07:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0015_automationdata_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='automationdata',
            name='entry_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
