# Generated by Django 5.0.2 on 2024-02-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
