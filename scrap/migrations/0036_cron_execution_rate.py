# Generated by Django 2.2 on 2019-05-22 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0035_auto_20190522_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='cron',
            name='execution_rate',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]