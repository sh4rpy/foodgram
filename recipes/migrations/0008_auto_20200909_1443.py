# Generated by Django 3.1.1 on 2020-09-09 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20200909_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Название'),
        ),
    ]
