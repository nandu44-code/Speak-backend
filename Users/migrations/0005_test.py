# Generated by Django 5.0.2 on 2024-02-23 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_alter_customuser_profile_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.CharField()),
            ],
        ),
    ]
