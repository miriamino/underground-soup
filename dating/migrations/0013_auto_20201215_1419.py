# Generated by Django 3.1.4 on 2020-12-15 13:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0012_auto_20201215_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 15, 13, 19, 47, 36749, tzinfo=utc), verbose_name='date answered'),
        ),
    ]