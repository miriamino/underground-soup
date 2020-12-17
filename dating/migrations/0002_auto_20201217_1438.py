# Generated by Django 3.1.4 on 2020-12-17 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='importance',
            field=models.IntegerField(choices=[(0, "doesn't matter at all"), (1, 'a little'), (50, 'average'), (250, 'very important'), (300, 'mandatory')], default=50),
        ),
    ]