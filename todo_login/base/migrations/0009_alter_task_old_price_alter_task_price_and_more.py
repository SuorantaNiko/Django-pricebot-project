# Generated by Django 4.0.2 on 2022-04-28 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_rename_prices_task_old_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='old_price',
            field=models.IntegerField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='price',
            field=models.IntegerField(blank=True, max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='wishPrice',
            field=models.IntegerField(blank=True, max_length=2000, null=True),
        ),
    ]