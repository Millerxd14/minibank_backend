# Generated by Django 3.2.4 on 2023-03-18 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cuenta', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuenta',
            old_name='usuario',
            new_name='user',
        ),
    ]
