# Generated by Django 5.0.2 on 2024-02-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
