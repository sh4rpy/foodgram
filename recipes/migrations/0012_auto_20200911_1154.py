# Generated by Django 3.1.1 on 2020-09-11 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_auto_20200910_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe'),
        ),
    ]
