# Generated by Django 5.0.6 on 2024-07-04 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_rename_metro_savedjob_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='link',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='savedjob',
            name='link',
            field=models.CharField(max_length=500),
        ),
    ]
