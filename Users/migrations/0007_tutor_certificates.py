# Generated by Django 5.0.2 on 2024-02-26 09:09

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_delete_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='certificates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, default=list, size=None),
        ),
    ]
