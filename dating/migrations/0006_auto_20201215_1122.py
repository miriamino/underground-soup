# Generated by Django 3.1.4 on 2020-12-15 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating', '0005_auto_20201214_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='answer_other',
            field=models.ManyToManyField(related_name='answer', to='dating.Choice'),
        ),
        migrations.AddField(
            model_name='choice',
            name='importance',
            field=models.IntegerField(choices=[(0, "doesn't matter at all"), (1, 'a little'), (50, 'average'), (250, 'very important'), (999, "don't show my profile to people who selected this")], default=-999),
        ),
    ]