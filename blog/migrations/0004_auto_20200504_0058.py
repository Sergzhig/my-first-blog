# Generated by Django 3.0.5 on 2020-05-03 21:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200504_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='update_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
