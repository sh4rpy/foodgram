# Generated by Django 3.1.1 on 2020-09-09 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20200909_1404'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='name',
            new_name='title',
        ),
    ]
