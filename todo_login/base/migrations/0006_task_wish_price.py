# Generated by Django 4.0.2 on 2022-03-27 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_task_prices'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='wish_price',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]
