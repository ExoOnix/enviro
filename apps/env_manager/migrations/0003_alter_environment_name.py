# Generated by Django 5.2.1 on 2025-06-01 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('env_manager', '0002_alter_environment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='environment',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
