# Generated by Django 4.0.2 on 2022-03-27 15:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_task_wish_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='wish_price',
            new_name='wishPrice',
        ),
    ]
