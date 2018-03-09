# Generated by Django 2.0.3 on 2018-03-09 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
        ('seekers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seeker',
            name='facebook_id',
            field=models.BigIntegerField(default=-2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seeker',
            name='jobs',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='jobs.Job'),
            preserve_default=False,
        ),
    ]
