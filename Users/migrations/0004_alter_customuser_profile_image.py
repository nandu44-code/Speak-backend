# Generated by Django 5.0.2 on 2024-02-23 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.TextField(blank=True),
        ),
    ]
