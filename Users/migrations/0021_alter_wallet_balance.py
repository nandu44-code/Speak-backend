# Generated by Django 5.0.2 on 2024-05-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0020_alter_tutor_dialect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.IntegerField(default=0),
        ),
    ]