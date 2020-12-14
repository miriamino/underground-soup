# Generated by Django 3.1.4 on 2020-12-14 18:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dating', '0004_auto_20201214_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer_self', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dating.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dating.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='userresponseself',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='userresponseself',
            name='question',
        ),
        migrations.RemoveField(
            model_name='userresponseself',
            name='user',
        ),
        migrations.DeleteModel(
            name='UserResponseOther',
        ),
        migrations.DeleteModel(
            name='UserResponseSelf',
        ),
    ]
